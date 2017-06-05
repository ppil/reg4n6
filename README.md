# Registry forensics for incident response

This program basically takes the path to a mounted Windows volume as input, finds and opens the registry hives within it, then runs various modules against them to produce an easy to read tabular report. By searching through all hives at the same time, artifacts from various locations can be correlated within the same table to add further insight into what's going on at a glance.

Various tools already exist (huge props to Carvey) to tear apart registry hives during an investigation. The reason I started writing this was primarily to learn more about analyzing Windows registry myself, but it eventually became clear that I could maybe fill a few gaps in functionality throughout the current open-source toolchest. My thought was that response times could be made significantly shorter by automatically locating all relevant hives, accessing any or all at the same time, and producing an easy to ready and navigate report. In this manner, registry analysis could even be automated and worked into a pre-investigative assessment of an image.


Usage: ./reg4n6.py --mount <mount_dir>  
  
-o [filename], --output [filename]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify output file. Default: STDOUT  
-f [fmt], --format [fmt]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify output format. Default: ASCII  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Supported formats: html, ascii  
-m [path], --mount [path]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify mount point of Windows OS  
--users [list,of,users]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify user(s) to focus on. Other ntuser hives are ignored.  
--ntuser [path]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify path to an ntuser hive. Can occur more than once.  
--system [path]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify path to system hive  
--software [path]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify path to software hive  
--sam [path]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specify path to sam hive  