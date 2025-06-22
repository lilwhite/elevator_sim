# tests/test_logger.py
from simulation.logger import Logger


def test_log_records_message_with_timestamp_and_level():
    ts = lambda: 42.0
    logger = Logger(log_level="INFO", timestamp_fn=ts)
    logger.log("Test message")
    logs = logger.show_history()
    assert len(logs) == 1
    entry = logs[0]
    assert entry.startswith("[42.0]")
    assert "INFO" in entry
    assert "Test message" in entry


def test_log_respects_log_level():
    ts = lambda: 0.0
    logger = Logger(log_level="WARNING", timestamp_fn=ts)
    logger.log("Info msg", level="INFO")
    logger.log("Warning msg", level="WARNING")
    logs = logger.show_history()
    assert len(logs) == 1
    assert "Warning msg" in logs[0]


def test_clear_clears_logs():
    logger = Logger()
    logger.log("A")
    logger.clear()
    assert logger.show_history() == []


def test_enable_disable():
    ts = lambda: 1.0
    logger = Logger(timestamp_fn=ts)
    logger.disable()
    logger.log("Should not log")
    assert logger.show_history() == []
    logger.enable()
    logger.log("Now logs")
    assert len(logger.show_history()) == 1


def test_set_level_changes_threshold():
    ts = lambda: 0.0
    logger = Logger(log_level="WARNING", timestamp_fn=ts)
    logger.set_level("ERROR")
    logger.log("Warn", level="WARNING")
    logger.log("Err", level="ERROR")
    logs = logger.show_history()
    assert len(logs) == 1
    assert "Err" in logs[0]


def test_export_writes_file(tmp_path):
    logger = Logger(timestamp_fn=lambda: 5.0)
    logger.log("Msg1", level="INFO")
    path = tmp_path / "log.txt"
    logger.export(str(path))
    assert path.exists()
    content = path.read_text()
    assert "Msg1" in content
