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
	@echo "table_errorbar.scr        o2graph.rst"
	@echo "table_plot.scr            o2graph.rst"
	@echo "table_plotv.scr           o2graph.rst"
	@echo "table_rplot.scr           o2graph.rst"
	@echo "table_scatter.scr         o2graph.rst"
	@echo "table3d_den_plot.scr      o2graph.rst"
	@echo "textbox.scr               o2graph.rst"
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

convert:
	jupytext --to py skyrme.ipynb

# The yt_scatter script is included here but the other yt plots are
# not because they are more time-consuming.
all: subplots1 subplots2 subplots3 table_plot \
	table_plotv table_rplot table_scatter table3d_den_plot \
	table_errorbar textbox yt_scatter modax cmaps colors_near \
	markers

cmaps:
	./cmaps.scr
	convert +append ../figures/cmaps_doc.png cmaps.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

skyrme.ipynb: empty
	jupytext --to ipynb --set-kernel python3 --execute skyrme.py

empty:

colors_near:
	./colors_near.scr
	convert +append ../figures/near_blue_doc.png near_blue.png \
		temp1.png
	convert +append ../figures/near_hex_doc.png near_hex.png \
		temp2.png
	convert +append ../figures/near_rgb_doc.png near_rgb.png \
		temp3.png
	$(VIEW_COMMAND) temp1.png $(VIEW_SUFFIX)
	$(VIEW_COMMAND) temp2.png $(VIEW_SUFFIX)
	$(VIEW_COMMAND) temp3.png $(VIEW_SUFFIX)

markers:
	./markers.scr
	convert +append ../figures/markers_doc.png markers.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

modax:
	./modax.scr
	convert +append ../figures/modax_doc.png modax.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots1:
	./subplots1.scr
	convert +append ../figures/subplots1_doc.png subplots1.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots2:
	./subplots2.scr
	convert +append ../figures/subplots2_doc.png subplots2.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots3:
	./subplots3.scr
	convert +append ../figures/subplots3_doc.png subplots3.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_plot:
	./table_plot.scr
	convert +append ../figures/table_plot_doc.png table_plot.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_plotv:
	./table_plotv.scr
	convert +append ../figures/table_plotv_doc.png table_plotv.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_rplot:
	./table_rplot.scr
	convert +append ../figures/table_rplot_doc.png table_rplot.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_errorbar:
	./table_errorbar.scr
	convert +append ../figures/table_errorbar_doc.png table_errorbar.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

textbox:
	./textbox.scr
	convert +append ../figures/textbox_doc.png textbox.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_scatter:
	./table_scatter.scr
	convert +append ../figures/table_scatter_doc.png table_scatter.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table3d_den_plot:
	./table3d_den_plot.scr
	convert +append ../figures/table3d_den_plot_doc.png table3d_den_plot.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

yt_scatter:
	./yt_scatter.scr
	convert +append ../figures/yt_scatter_doc.png yt_scatter.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

yt_tg_multvol:
	./yt_tg_multvol.scr
	convert +append ../figures/yt_tg_multvol_doc.png yt_tg_multvol.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)
# Combine the still images into a single image for the documentation
	montage /tmp/yt_00.png /tmp/yt_25.png /tmp/yt_50.png \
	/tmp/yt_75.png -geometry 512x512 yt_tg_multvol.png	

