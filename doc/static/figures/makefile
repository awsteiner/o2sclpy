help:
	@echo "------------------------------------------------------"
	@echo "Makefile for example scripts and documentation figures"
	@echo "------------------------------------------------------"
	@echo ""
	@echo "The 'make all' target creates all figures and compares the "
	@echo "output images with their currently stored versions."
	@echo ""
	@echo "The current figure list along with the documentation "
	@echo "file where they are found is:"
	@echo ""
	@echo "------------------------- -----------"
	@echo "subplots1.scr             o2graph.rst"
	@echo "subplots2.scr             o2graph.rst"
	@echo "subplots3.scr             o2graph.rst"
	@echo "table_plot.scr            o2graph.rst"
	@echo "table_plotv.scr           o2graph.rst"
	@echo "table_rplot.scr           o2graph.rst"
	@echo "table_scatter.scr         o2graph.rst"
	@echo "table3d_den_plot.scr      o2graph.rst"
	@echo "yt_scatter.scr            yt.rst"
	@echo "yt_tg_multvol.scr         yt.rst"
	@echo ""
	@echo "The script 'backend.scr' does not generate any figures."
	@echo ""
	@echo "There are other experimental scripts which are not "
	@echo "yet included in the documentation."

UNAME := $(shell uname -s)

ifeq ($(UNAME),Linux)
VIEW_COMMAND = eog
VIEW_SUFFIX = &
else
VIEW_COMMAND = open
VIEW_SUFFIX = 
endif

all: subplots1 subplots2 subplots3 table_plot \
	table_plotv table_rplot table_scatter table3d_den_plot

subplots1:
	./subplots1.scr
	convert +append subplots1_doc.png subplots1.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots2:
	./subplots2.scr
	convert +append subplots2_doc.png subplots2.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots3:
	./subplots3.scr
	convert +append subplots3_doc.png subplots3.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_plot:
	./table_plot.scr
	convert +append table_plot_doc.png table_plot.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_plotv:
	./table_plotv.scr
	convert +append table_plotv_doc.png table_plotv.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_rplot:
	./table_rplot.scr
	convert +append table_rplot_doc.png table_rplot.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_scatter:
	./table_scatter.scr
	convert +append table_scatter_doc.png table_scatter.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table3d_den_plot:
	./table3d_den_plot.scr
	convert +append table3d_den_plot_doc.png table3d_den_plot.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

yt_scatter:
	./yt_scatter.scr
	convert +append yt_scatter_doc.png yt_scatter.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

yt_tg_multvol:
	./yt_tg_multvol.scr
	convert +append yt_tg_multvol_doc.png yt_tg_multvol.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)
# Combine the still images into a single image for the documentation
	montage /tmp/yt_00.png /tmp/yt_25.png /tmp/yt_50.png \
	/tmp/yt_75.png -geometry 512x512 yt_tg_multvol.png	

