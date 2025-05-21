from anus.core.orchestrator import AgentOrchestrator


def test_orchestrator_startup():
    orch = AgentOrchestrator(config_path="config.yaml")
    assert orch.primary_agent is not None

