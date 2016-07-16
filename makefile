build:
	@>diagrammer
	@cat src/* >> diagrammer
	@echo "if __name__ == \"__main__\": main()" >> diagrammer
.PHONY: build
