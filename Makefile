all:
	./SimpleServer.py

test:
	./edgecover.py

clean:
	-rm gurobi.log *.pyc *.lp
