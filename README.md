# phyllo-python

[Phyllo](https://github.com/ethanjli/phyllo) is a point-to-point communication protocol suite and application framework specification designed for use with embedded systems.

Phyllo provides a specification for high-throughput + reliable + asynchronous message exchange between exactly two (2) peers. Phyllo also provides a specification for applications to communicate with each other across a pair of hosts (which may be either an embedded device or a regular computer) or distributed across multiple hosts.

Phyllo-python is a reference implementation in Python 3.5+ as a library for use on computers.


## Design

Each layer of the phyllo protocol stack implementation follows [Sans I/O](https://sans-io.readthedocs.io) principles, so the protocol itself works regardless of the method used for sending and receiving data. This means that it can be placed on top of any communication layer which provides a programming interface for either:
- Sending and receiving bytes over a stream, or
- Sending and receiving discrete units of data (e.g. frames or datagrams or Python data structures) over a message-oriented communication link

Each layer is a phylline link; for message-oriented layers, the layer exposes `receive` and `send` methods on top and `to_receive` and `to_send` methods below for data flowing up and down the stack, respectively.

Separately from the protocol stack, phyllo also provides an easy way to place its protocol stack on top of a [UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) serial connection, such as with a USB cable between a computer and an Arduino or an RX/TX wire pair between a Raspberry Pi and an Arduino. The protocol stack is designed to be easily placeable on top of other types of connections in the future and to be easily used with different methods of flow control (e.g. polling for new data in a single thread or receiving new data in a background thread).


## Functionality and Limitations

Because phyllo's development is driven by the needs of other ongoing projects, its development prioritizes the need of those projects. Here are phyllo's functionalities and limitations in order of higher priority to lower priority.

Currently, phyllo does:

- Implement ChunkedStreamLink.
- Implement FrameLink.
- Implement DatagramLink.
- Implement ValidatedDatagramLink.
- Partially ReliableBufferLink.
- Implement DocumentLink.
- Implement Pub-Sub Framework's MessageLink and DocumentLink and EndpointHandler.
- Provide polling-based and threading-based interfaces for serial I/O.
- Have moderate test coverage.

Currently, phyllo-python does not yet:
- Fully implement ReliableBufferLink.
- Have high test coverage.
- Implement a way to report errors at the protocol level in DatagramLink or above.
- Provide documentation of protocol implementation APIs.
- Have a first alpha release.
- Implement robust fault detection and handling in the transport or application layers.

Phyllo-python does not yet (and will not, unless you'd like to make a feature request and start a discussion):
- Provide adaptors to transport documents or commands directly on a python [multiprocessing.Queue](https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.Queue).
- Provide adaptors to transport data over local inter-process communication mechanisms (e.g. Unix domain sockets or pipes).
- Provide adaptors to transport documents or commands over reliable application-layer internet protocols (e.g. MQTT, WebSocket).
- Provide asynchronous interfaces (e.g. via asyncio or trio) for serial I/O.


## Performance

TBD


## Related Projects

The following libraries also provide network protocol stacks to enable reliable message exchange on embedded devices:
- [PJON](https://www.pjon.org) ([Github](https://github.com/gioblu/PJON)) enables communication between two or more devices, potentially on a network, over any of *a variety of media and transports*. Note that the [python library](https://github.com/Girgitt/PJON-python) is not actively developed and only has a minimal client operational with PJON v4.2 or v4.3, while PJON itself is at v11.2. However, there is also a [cython-based python library](https://github.com/xlfe/PJON-cython) which supports PJON v11.2 with UDP and Serial transports.
- [RadioHead](https://www.airspayce.com/mikem/arduino/RadioHead/) is a network protocol stack designed to provide to enable communication between two or more devices, potentially on a network, over *any of a variety of data radios* and other transports. Note that serial communication from a computer is only supported by a C++ library.


## Installation


Install this package as you would any other package. Note that, to support serial I/O, you will need to install with the `serial` extra. For example, in pip:

```
pip install phyllo[serial]
```


## Unit Tests
Unit tests can be run with the `pytest` command from the repository directory.
This will require installation of the packages listed in `tests/requirements.txt`.
Then you can take advantage of the following features:

- Show test errors immediately, rather than at the end of testing.
- Generate an HTML report at `testreport.html`
- Run tests in parallel with the `-n NUM` argument.
- Run tests related to modified files (as determined by Git) before all other tests with the `--picked=first` argument, and run only tests related to modified files with the `--picked`. By default, "modified files" is releative to unstaged files, but pytest will reinterpret it as relative to the base of the current branch with `--mode=branch`.
- Summarize gaps in test coverage with the `--cov=phyllo --cov-branch --cov-report term-missing:skip-covered` arguments; add the `--cov-report html` argument to also generate an html report at `htmlcov/index.html`. Note that if you use these when tests are run in parallel, you may get a warning that no coverage was collected.
- Show a summary of Hypothesis fuzz tests with the `--hypothesis-show-statistics` argument.
- Perform performance profiling with `--profile --profile-svg`. The report is generated to `prof/combined.svg`.

as well as the following built-in features which come with pytest:

- List each individual test with `--verbose`. Note that output is cleaner when tests are *not* run in parallel.
- Only run previously failed tests with `--last-failed`.
- Run previously failed tests before other tests with `--failed-first`.
- Switch to pdb on the first failure with `--pdb  -x`
- Report how long each test took to run with `--durations=0`

For example, to run all tests quickly, prioritizing changed files and previously failed tests, use either of the two following equivalent commands:
```
pytest --picked=first --failed-first -n auto
python3 setup.py test_quick
```
For example, to run only tests for files with modifications since the base of the current Git branch,
prioritizing changed files, use either of the two following equivalent commands:
```
pytest --picked --mode=branch --failed-first -n auto
python3 setup.py test_quick_branch
```
For example, to switch to pdb on the first failure, use either of the two following equivalent commands:
```
pytest --picked=first --failed-first --pdb -x
python3 setup.py test_debug
```
For example, to do performance profiling, use either of the two following equivalent commands:
```
pytest --profile --profile-svg
python3 setup.py test_perf
```
For example, to get a coverage summary, use either of the two following equivalent commands:
```
pytest --cov=camlab_headform --cov-branch --cov-report term-missing:skip-covered --cov-report html
python3 setup.py test_coverage
```
The most complete report can be obtained with either of the two following equivalent commands:
```
pytest --durations=0 --cov=camlab_headform --cov-branch --cov-report term-missing --cov-report html --hypothesis-show-statistics --verbose
python3 setup.py test_complete
```
