default: build run
build:
	@>diagrammer
	@cat src/* >> diagrammer
	@echo "if __name__ == \"__main__\": main()" >> diagrammer
run:
	@./diagrammer file.dia
.PHONY: default build run
