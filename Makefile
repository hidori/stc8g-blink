.DEFAULT_GOAL := build

PIO_BIN ?= $(HOME)/.platformio/penv/bin/pio

.PHONY: build deploy clean prepare/ide

build:
	$(PIO_BIN) run

deploy:
	pkill -f '[p]io run --target upload|[s]tcgal(_stc8g)?\.py' || true
	$(PIO_BIN) run --target upload

clean:
	$(PIO_BIN) run --target clean

prepare/ide:
	$(PIO_BIN) project init --ide vscode
