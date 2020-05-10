CXX = g++
CFLAGS = -g -pg -Wall -Wextra -Werror -std=c++17 -O2 $(shell curl-config --cflags)

CRAWLER = \
					obj/crawler/main.o

TWIRL = \
				obj/twirl/twirl.o \
				obj/twirl/twirl_response.o


HDR = $(shell ls src/**/*.hpp)
OBJ = $(CRAWLER) $(TWIRL)
LINK = -lpthread $(shell curl-config --libs)
DEFS =

.SECONDARY:

obj/%.o: src/%.cpp $(HDR)
	@echo -e "\u001b[33mASSEMBLING OBJECT $@\u001b[0m"
	@mkdir -p `dirname $@`
	@$(CXX) $(CFLAGS) $(DEFS) $< -c -o $@


.PHONY: all

all: thou_crawler

thou_crawler: $(CRAWLER) $(OBJ) $(HDR)
	@echo -e "\u001b[34mLINKING OBJECTS TO EXECUTABLE $@\u001b[0m"
	@$(CXX) $(CFLAGS) $(DEFS) $(CLIENT) $(OBJ) -o $@ $(LINK)


prof_pdf:
	gprof thou_crawler gmon.out > analysis.txt
	gprof2dot -o d.dot analysis.txt
	dot -Tpdf d.dot > prof.pdf


clean:
	rm -rf obj thou_crawler thou_server
