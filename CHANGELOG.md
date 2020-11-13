# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - 13 November 2020
### Changed
- Updated AbstractRepository to save class-level keyword arguments so they can be used
  by subclasses if needed
- Moved repository instantiation in BaseUnitOfWork from __init__() to __aenter__() to
  allow subclasses to manipulate arguments that are passed into repositories

## [0.2.0] - 12 November 2020
### Added
- add_dependencies() method to MessageBus class
- __repr__() method to AbstractRepository, BaseUnitOfWork, and Entity