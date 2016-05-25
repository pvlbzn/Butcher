# Butcher

Butcher is an image cutter dedicated to prepare graphics for Android platform.

### Structure
This repository contains two library-like implemintations: Python, Go. They produces almost the similar result. Almost because Python's uses `PIL`, Golang's uses `nfnt/resize` realization, thus results may vary.

```
.
├── README.md
├── gobutcher
│   ├── butcher.go
│   └── butcher_test.go
└── pybutcher
    ├── butcher.py
    └── test_butcher.py
```

### gobutcher

```
.
├── butcher.go
└── butcher_test.go
```

Go's implementation contains library and tests for it. All tests are passing.

```
$ go test

PASS
ok  	github.com/pvlbzn/butcher/gobutcher	0.119s
```

### pybutcher

```
.
├── butcher.py
└── test_butcher.py
```

Python's implementation contains library and tests for it. All tests are passing.

```
$ py.test

=========================== 3 passed in 0.13 seconds ===========================
```


### Status
Project is ready to use, works well, produces good results. However it lacks any CLI or interface, these only libraries. May be I'll write CLIs, but may be not, so you are very welcome to fork.

<br>

### TODO

- Add CLI
