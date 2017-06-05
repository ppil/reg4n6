#!/usr/bin/python

import sys
import cgi

def write_html_table(title, rows, out=sys.stdout):
	if title:
		html = "<h2 id=%s>%s</h2>\n<table>\n"%(title.replace(' ',''),title)
	else:
		html = "<table>\n"
	# Add header
	html += "<tr>\n"
	for col in rows[0]:
		html += "\t<th>%s</th>\n"%col
	html +=  "</tr>"
	# Add data
	for row in rows[1:]:
		html += "<tr>\n"
		for col in row:
			html += "\t<td>%s</td>\n"%cgi.escape(col)
		html += "</tr>"
	html += "</table>\n<br>\n"
	out.write(html)
	

def write_html_vals(title, rows, out=sys.stdout):
	if title:
		html = "<h2 id=%s>%s</h2>\n"%(title.replace(' ',''), title)
	else:
		html = ""
	left_width = max_row_width(rows, 0)+2
	right_width = max_row_width(rows, 1)
	for i, col in enumerate(rows[0]):
		html += "<div style='margin-left:3%%;width:%dch'><b>%s:</b></div><div style='width:%dch'>%s&nbsp;</div><br>\n"%(left_width,cgi.escape(rows[0][i]),right_width,cgi.escape(rows[1][i]))
	html += "<br>\n"
	out.write(html)
	
def write_std_table(title, rows, out=sys.stdout):
	padding=[]
	for i in range(len(rows[0])):
		padding.append(max_col_width(rows, i))
	if title:
		out.write("\n\n\t%s\n\n"%title)
	else:
		out.write("\n")
	for i, row in enumerate(rows):
		if i == 1: # Add a divider
			out.write("-"*(sum(padding)+2*len(padding))+"\n")
		for i, col in enumerate(row):
			out.write(col.ljust(padding[i]+2))
		out.write("\n")
		
def write_std_vals(title, rows, out=sys.stdout):
	left_width = max_row_width(rows,0)
	if title:
		out.write("\n\n\t%s\n\n"%title)
	else:
		out.write("\n")
	for i, col in enumerate(rows[0]):
		out.write(rows[0][i].ljust(left_width+2, '.'))
		out.write(": "+rows[1][i]+"\n")

def max_col_width(rows, col):
	return max([len(row[col]) for row in rows])

def max_row_width(rows,row):
	return max([len(entry) for entry in rows[row]])

def dict_to_arr(rows, pairs):
	if pairs:
		rows.append([])
		for col in rows[0]:
			if col not in pairs.keys():
				rows[-1].append("")
			else:
				rows[-1].append(str(pairs[col]))

def sort_by_col(rows, key):
	for i, col in enumerate(rows[0]):
		if col == key:
			return [rows[0]] + sorted(rows[1:], key=lambda x: x[i])
	return rows

def write_out(cfg, rows, title, table=0):
	if len(rows) > 1:
		if title != '':
			cfg['titles'].append(title)
		if cfg["format"] == "ascii":
			if table:
				write_std_table(title, rows, cfg["outfh"])
			else:
				write_std_vals(title, rows, cfg["outfh"])
		elif cfg["format"] == "html":
			if table:
				write_html_table(title, rows, cfg["outfh"])
			else:
				write_html_vals(title, rows, cfg["outfh"])
