default: build run
build:
	@>diagrammer
	@cat src/* >> diagrammer
	@echo "if __name__ == \"__main__\": main()" >> diagrammer
run:
	@./diagrammer file.dia
update: build
	@gksudo cp diagrammer /usr/bin/diagrammer
.PHONY: default build run update
