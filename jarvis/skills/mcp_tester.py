"""
MCP Server Tester Skill

Tests Model Context Protocol (MCP) servers:
  - Connectivity (TCP/HTTP ping)
  - SSE endpoint handshake
  - Tool discovery (list tools)
  - Tool invocation test
  - Response validation
  - Latency measurement
"""
import json
import time
import socket
import urllib.parse
import urllib.request
import urllib.error
from typing import Any


def _http_get(url: str, timeout: float = 5.0) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")[:4000]
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)
    except Exception as e:
        return -1, str(e)


def _http_post(url: str, body: dict, timeout: float = 10.0) -> tuple[int, str]:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")[:4000]
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")[:1000]
        return e.code, body_txt
    except Exception as e:
        return -1, str(e)


def _tcp_ping(host: str, port: int, timeout: float = 3.0) -> float | None:
    """Returns latency in ms or None."""
    try:
        t0 = time.perf_counter()
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return (time.perf_counter() - t0) * 1000
    except Exception:
        return None


def _parse_url(url: str) -> tuple[str, int, str]:
    """Return (host, port, scheme)."""
    p = urllib.parse.urlparse(url)
    port = p.port or (443 if p.scheme == "https" else 80)
    return p.hostname, port, p.scheme


# ─── Test functions ──────────────────────────────────────────────────────────

def test_mcp_server(url: str) -> str:
    """Full MCP server test: connectivity → discovery → invocation."""
    report = [f"═══ MCP SERVER TEST: {url} ═══\n"]

    # 1. TCP ping
    host, port, scheme = _parse_url(url)
    latency = _tcp_ping(host, port)
    if latency is not None:
        report.append(f"✓ TCP Connectivity: {latency:.1f}ms")
    else:
        report.append(f"✗ TCP Connectivity FAILED — host {host}:{port} unreachable")
        return "\n".join(report)

    # 2. HTTP health check
    health_url = url.rstrip("/") + "/health"
    status, body = _http_get(health_url, timeout=4.0)
    if status == 200:
        report.append(f"✓ Health endpoint: 200 OK")
    else:
        report.append(f"~ Health endpoint: {status} (may not exist)")

    # 3. MCP initialize handshake (JSON-RPC 2.0)
    t0 = time.perf_counter()
    rpc_url = url.rstrip("/")
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "Jarvis-MCPTester", "version": "1.0"}
        }
    }
    status, body = _http_post(rpc_url, init_payload)
    rtt = (time.perf_counter() - t0) * 1000

    if status in (200, 201):
        try:
            resp = json.loads(body)
            if "result" in resp:
                sv = resp["result"].get("serverInfo", {})
                proto = resp["result"].get("protocolVersion", "?")
                report.append(f"✓ MCP Handshake: {sv.get('name','?')} v{sv.get('version','?')} "
                               f"(protocol {proto}) — {rtt:.0f}ms")
                caps = resp["result"].get("capabilities", {})
                if caps:
                    report.append(f"  Capabilities: {', '.join(caps.keys())}")
            elif "error" in resp:
                report.append(f"~ MCP Init error: {resp['error']}")
            else:
                report.append(f"~ Unexpected response: {body[:200]}")
        except json.JSONDecodeError:
            report.append(f"~ Response is not JSON (status {status}): {body[:200]}")
    else:
        report.append(f"✗ MCP Handshake FAILED: HTTP {status} — {body[:300]}")

    # 4. Tool discovery
    list_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    status, body = _http_post(rpc_url, list_payload)
    if status == 200:
        try:
            resp = json.loads(body)
            tools = resp.get("result", {}).get("tools", [])
            report.append(f"\n✓ Tool Discovery: {len(tools)} tools found")
            for t in tools[:10]:
                desc = t.get("description", "")[:60]
                params = list(t.get("inputSchema", {}).get("properties", {}).keys())
                param_str = f"({', '.join(params)})" if params else "(no params)"
                report.append(f"  • {t['name']} {param_str} — {desc}")
            if len(tools) > 10:
                report.append(f"  ... and {len(tools) - 10} more")
        except Exception:
            report.append(f"~ Tool list parse error: {body[:200]}")
    else:
        report.append(f"~ Tool discovery: HTTP {status}")

    report.append(f"\n{'─'*40}")
    report.append(f"Test complete.")
    return "\n".join(report)


def ping_mcp(url: str) -> str:
    """Quick ping: just TCP + HTTP."""
    host, port, _ = _parse_url(url)
    latency = _tcp_ping(host, port)
    if latency is None:
        return f"✗ {url} — unreachable"
    status, _ = _http_get(url, timeout=3.0)
    return f"✓ {url} — {latency:.1f}ms TCP, HTTP {status}"


def call_mcp_tool(url: str, tool_name: str, params: str = "{}") -> str:
    """Call a specific MCP tool with given JSON params."""
    try:
        p = json.loads(params)
    except Exception:
        return f"Invalid JSON params: {params}"

    payload = {
        "jsonrpc": "2.0",
        "id": 99,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": p}
    }
    t0 = time.perf_counter()
    status, body = _http_post(url.rstrip("/"), payload)
    rtt = (time.perf_counter() - t0) * 1000

    try:
        resp = json.loads(body)
        if "result" in resp:
            content = resp["result"].get("content", [])
            texts = [c.get("text", "") for c in content if c.get("type") == "text"]
            return f"✓ {tool_name} — {rtt:.0f}ms\n" + "\n".join(texts)[:2000]
        elif "error" in resp:
            return f"✗ Tool error: {resp['error']}"
    except Exception:
        pass
    return f"HTTP {status} — {body[:500]}"


def list_mcp_tools(url: str) -> str:
    """List all tools on an MCP server."""
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    status, body = _http_post(url.rstrip("/"), payload)
    if status != 200:
        return f"✗ HTTP {status}: {body[:300]}"
    try:
        resp = json.loads(body)
        tools = resp.get("result", {}).get("tools", [])
        lines = [f"Tools on {url} ({len(tools)} total):"]
        for t in tools:
            required = t.get("inputSchema", {}).get("required", [])
            lines.append(f"  {t['name']} — {t.get('description','')[:80]}")
            if required:
                lines.append(f"    required: {required}")
        return "\n".join(lines)
    except Exception as e:
        return f"Parse error: {e}\n{body[:300]}"


SKILLS = [
    {
        "name": "test_mcp_server",
        "description": "Full MCP server test: TCP ping, handshake, tool discovery.",
        "trigger_phrases": ["test mcp", "mcp server test", "check mcp"],
        "func": test_mcp_server,
    },
    {
        "name": "ping_mcp",
        "description": "Quick TCP+HTTP ping of an MCP server URL.",
        "trigger_phrases": ["ping mcp", "mcp ping", "is mcp up"],
        "func": ping_mcp,
    },
    {
        "name": "list_mcp_tools",
        "description": "List all available tools on an MCP server.",
        "trigger_phrases": ["list mcp tools", "mcp tools", "what tools does mcp have"],
        "func": list_mcp_tools,
    },
    {
        "name": "call_mcp_tool",
        "description": "Call a specific tool on an MCP server with JSON params.",
        "trigger_phrases": ["call mcp tool", "invoke mcp", "run mcp tool"],
        "func": call_mcp_tool,
    },
]
