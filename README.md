# cfg_to_xlsx

Tachnican in charge of Scada (Siemens Simatic) wanted help from me. 

problem : He prepare xls table about electrik panel map for electricic technician. He need to write every cell with hand one by one. This operation takes approximately 4 hours. I tried to decrease this preparing time 2 second.

Program Steps: 

<ul>
  <li>Pandas read .cfg file in lines</li>
  <li>I developed an algorithm for searching in lines according to panel numbers</li>
  <ul>
    <li> I collected every useful lines index numbers in a list</li>
    <li> I matched the index numbers with orjinals lines and create a new list including strings</li>
    <li> I repeated this process 4 times for every type of data</li>
  </ul>
  <li>I concat whole seperated data and record it as an xls file</li>
  <li> I used PyQT5 for design interface in another python file in the name"cfg_to_xls.py" </li>
  <li> I brought an exe file to py files with "pyinstaller"</li>
</ul>
<hr>
  <em>
  Aydin Aktar
  <br>
  Mİneral Processing Engineer</li>
  </em>

