//@flow
"use strict";

import React from 'react';
import ReactDOM from 'react-dom'
import GBEXtable from './components/GBEXtable'
import './css/mytable.css'

/*
window.table_settings is a json object

{
  'table_name_1': {
    'window.column_widths': {
      'column_name_1': number,
      'column_name_2': number,
      etc
    },
    'window.column_shows': [
      'column_name_1',
      'column_name_2',
      etc
    ]
  },
  'table_name_2': etc,
}

*/

window.column_widths = "col_widths";
window.column_shows = "col_shows";
window.table_settings = {};
window.table_settings[window.whodis] = {};
window.table_settings[window.whodis][window.column_widths] = Object.assign({}, ...window.columns.map(d => ({[d]: d.length*12+50}))); //default widhts based on name length
let custom_cws = {
    "Oligo": {"name": 235, "responsible": 199, "Usage": 349, "OligoType": 158, "Sequence": 614},
    "Plasmid": {"name": 232, "responsible": 182, "Usage": 212, "GenbankFile": 182},
    "RawResult": {"name": 148, "responsible": 182, "Description": 259, "ResultType": 170, "DataFile": 299},
    "Experiment": {"name": 148, "responsible": 182, "Description": 304, "Oligos": 718, "Plasmids": 349, "Results": 134}
}
window.table_settings[window.whodis][window.column_widths] = custom_cws[window.whodis]
window.table_settings[window.whodis][window.column_shows] = [...window.columns]; //default show all

ReactDOM.render(
  <GBEXtable
    InitialColumnWidths={window.table_settings[window.whodis][window.column_widths]}
    InitialColumnVisible={window.table_settings[window.whodis][window.column_shows]} />,
  document.getElementById('root')
);
