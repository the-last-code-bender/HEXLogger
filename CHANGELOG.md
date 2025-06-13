# 📜 `CHANGELOG`  
```markdown
## [v2.0.0] - 2025-06-13
### Added
- Auto-start/stop logging option based on data inactivity (timeout)
- Timeout tracking only starts **after the first data is received**
- Optional filename counter (`001`, `002`, ...) for each auto-split file

### Changed
- Unified filename logic under selected config name
- Improved console prompts and user interaction (all in English)
```

```markdown
## [v1.1.0] - 2025-06-10
### Added
- Increased Rx and Tx buffer sizes.
- Improved handling when port is not found (do not close immediately).
- Embedded config name into the binary file name.
```

```markdown
## [v1.0.0] - 2025-06-05
### Added
- Initial release with serial port listing and selection
- Configurable baudrate, stopbits, bytesize, parity, flow control
- Support for configuration via `config.json` or manual input
- Real-time byte count feedback while logging
- Timestamped binary output file generation
- Keyboard-based logging termination
- Clean console UI with line clearing
- Windows terminal color support using `colorama`
```