help:
	@echo help

all: subplots1 subplots2 subplots3 table_plot table3d_den_plot \
	table_plotv table_rplot table_scatter

subplots1:
	./subplots1.scr
	convert +append subplots1_doc.png subplots1.png \
		temp.png
	open temp.png

subplots2:
	./subplots2.scr
	convert +append subplots2_doc.png subplots2.png \
		temp.png
	open temp.png

subplots3:
	./subplots3.scr
	convert +append subplots3_doc.png subplots3.png \
		temp.png
	open temp.png

table_plot:
	./table_plot.scr
	convert +append table_plot_doc.png table_plot.png \
		temp.png
	open temp.png

table3d_den_plot:
	./table3d_den_plot.scr
	convert +append table3d_den_plot_doc.png table3d_den_plot.png \
		temp.png
	open temp.png

table_plotv:
	./table_plotv.scr
	convert +append table_plotv_doc.png table_plotv.png \
		temp.png
	open temp.png

table_rplot:
	./table_rplot.scr
	convert +append table_rplot_doc.png table_rplot.png \
		temp.png
	open temp.png

table_scatter:
	./table_scatter.scr
	convert +append table_scatter_doc.png table_scatter.png \
		temp.png
	open temp.png


