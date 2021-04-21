# OpenSight Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.4] - 2021-04-21
### Added
- Transaction details now work with CoinBase transactions

### Changed
- UTXOs now returned in reverse order (consistent with rest.bitcoin.com)

### Fixed
- Add proper error handling
- Add ‘retry’ for calls that sometimes fail when communicating with node or Electrum
- Fix incorrectly calculated floating point numbers

## [1.0.3]
### Added
- Add unit tests

### Fixed
- Fix receive bytes from Electrum server

## [1.0.2]
### Added
- Add environmental variable configuration options

### Changed
- Reduce Docker image size by using Alpine image



