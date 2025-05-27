help:
	@echo "------------------------------------------------------"
	@echo "Makefile for example scripts and documentation figures"
	@echo "------------------------------------------------------"
	@echo ""
	@echo "make targets     descriptions"
	@echo "--------------   ------------"
	@echo "help             output this makefile information"
	@echo ""

UNAME := $(shell uname -s)

ifeq ($(UNAME),Linux)
VIEW_COMMAND = eog
VIEW_SUFFIX = &
else
VIEW_COMMAND = open
VIEW_SUFFIX = 
endif

make_readme:
	$(MAKE) help > README.md

# The yt_scatter script is included here but the other yt plots are
# not because they are more time-consuming.
all: subplots1 subplots2 subplots3 table_plot \
	table_plotv table_rplot table_scatter table3d_den_plot \
	table_errorbar textbox yt_scatter modax cmaps colors_near \
	markers

skyrme.ipynb: empty
	jupytext --to ipynb --update skyrme.py 

interpm.ipynb: empty
	jupytext --to ipynb --update interpm.py 

DSH.ipynb: empty
	jupytext --to ipynb --update DSH.py 

table.ipynb: empty
	jupytext --to ipynb --update table.py 

tov.ipynb: empty
	jupytext --to ipynb --update tov.py 

unit_conv.ipynb: empty
	jupytext --to ipynb --update unit_conv.py 

link_o2scl.ipynb: empty
	jupytext --to ipynb --update link_o2scl.py 

nucmass.ipynb: empty
	jupytext --to ipynb --update nucmass.py 

SFHo_SFHx.ipynb: empty
	jupytext --to ipynb --update SFHo_SFHx.py 

buchdahl.ipynb: empty
	jupytext --to ipynb --update buchdahl.py 

empty:

cmaps:
	./cmaps.scr
	o2graph -append-images ../doc/static/figures/cmaps.png cmaps.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

colors_near:
	./colors_near.scr
	o2graph -append-images ../doc/static/figures/near_blue.png \
		near_blue.png temp1.png
	o2graph -append-images ../doc/static/figures/near_hex.png \
		near_hex.png temp2.png
	o2graph -append-images ../doc/static/figures/near_rgb.png \
		near_rgb.png temp3.png
	$(VIEW_COMMAND) temp1.png $(VIEW_SUFFIX)
	$(VIEW_COMMAND) temp2.png $(VIEW_SUFFIX)
	$(VIEW_COMMAND) temp3.png $(VIEW_SUFFIX)

markers:
	./markers.scr
	o2graph -append-images ../doc/static/figures/markers.png \
		markers.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

modax:
	./modax.scr
	o2graph -append-images ../doc/static/figures/modax.png \
		modax.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots1:
	./subplots1.scr
	o2graph -append-images ../doc/static/figures/subplots1.png \
		subplots1.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots2:
	./subplots2.scr
	o2graph -append-images ../doc/static/figures/subplots2.png \
		subplots2.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

subplots3:
	./subplots3.scr
	o2graph -append-images ../doc/static/figures/subplots3.png \
		subplots3.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_plot:
	./table_plot.scr
	o2graph -append-images ../doc/static/figures/table_plot.png \
		table_plot.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_plotv:
	./table_plotv.scr
	o2graph -append-images ../doc/static/figures/table_plotv.png \
		table_plotv.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_rplot:
	./table_rplot.scr
	o2graph -append-images ../doc/static/figures/table_rplot.png \
		table_rplot.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_errorbar:
	./table_errorbar.scr
	o2graph -append-images ../doc/static/figures/table_errorbar.png \
		table_errorbar.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

textbox:
	./textbox.scr
	o2graph -append-images ../doc/static/figures/textbox.png textbox.png \
		temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table_scatter:
	./table_scatter.scr
	o2graph -append-images ../doc/static/figures/table_scatter.png \
		table_scatter.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

table3d_den_plot:
	./table3d_den_plot.scr
	o2graph -append-images ../doc/static/figures/table3d_den_plot.png \
		table3d_den_plot.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

yt_scatter:
	./yt_scatter.scr
	o2graph -append-images ../doc/static/figures/yt_scatter.png \
		yt_scatter.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)

yt_tg_multvol:
	./yt_tg_multvol.scr
	o2graph -append-images ../doc/static/figures/yt_tg_multvol.png \
		yt_tg_multvol.png temp.png
	$(VIEW_COMMAND) temp.png $(VIEW_SUFFIX)
# Combine the still images into a single image for the documentation
#	montage /tmp/yt_00.png /tmp/yt_25.png /tmp/yt_50.png \
#	/tmp/yt_75.png -geometry 512x512 yt_tg_multvol.png	

