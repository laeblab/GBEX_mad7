//@flow
"use strict";

import React from 'react';
import { Glyphicon } from 'react-bootstrap'
import { AutoSizer, MultiGrid } from 'react-virtualized';
import 'react-virtualized/styles.css'

const stlg = {zIndex: 2,boxShadow: "10px 10px 10px -5px #888"};
const strg = {zIndex: 1,boxShadow: "0px 10px 10px -5px #888"};
const sblg = {zIndex: 1,boxShadow: "10px 0px 10px -5px #888"};

type State = {
  scrollToColumn: number,
  scrollToRow: number,
  cursorColumn: number,
  cursorRow: number,
  editActive: boolean,
  dragCurrentX: number,
  dragTarget: string,
  dragStartX: number
}

type Props = {
  data: Array<Array<string>>,
  rowsSelected: Set<string>,
  rowsFoundSorted: Array<string>,
  columnVisible: Array<string>,
  columnWidths: Object,
  columnSearch: Object,
  columnFilter: Set<string>,
  searchCursor: string,
  doColumnResize: Function,
  onRowSelectChange: Function,
  onRowSelectToggleAll: Function,
  doFilter: Function,
  doSearch: Function,
  doSort: Function,
}

export default class RVMultiGrid extends React.PureComponent<Props, State> {
  state = {
    scrollToColumn: 1,            // currently scrolled to column
    scrollToRow: 1,               // currently scrolled to row
    cursorColumn: 1,              // currently selected column
    cursorRow: 1,                 // currently selected row
    dragCurrentX: -10,            // column resize drag visualizer
    dragTarget: "",               // who is being dragged?
    dragStartX: 0                 // where did we start draggin?
  };

  mugi: MultiGrid;                // multigrid ref
  aks: HTMLDivElement;            // keydown capture ref
  // ref setters
  _setMugi = (mugi: MultiGrid) => this.mugi = mugi;
  _setaks = (outer: HTMLDivElement) => this.aks = outer;

  _onMouseUp = (e) => {
    document.removeEventListener('mousemove', this._onMouseMove);
    document.removeEventListener('mouseup', this._onMouseUp);
    let new_col_width = e.clientX - this.state.dragStartX;
    this.props.doColumnResize(this.state.dragTarget, new_col_width);
  };

  _onMouseMove = (e) => {
    this.setState({dragCurrentX: e.clientX});
  };

  _columnDrag = (e: SyntheticDragEvent<HTMLDivElement>) => {
    document.addEventListener('mousemove', this._onMouseMove);
    document.addEventListener('mouseup', this._onMouseUp);
    // store current target name and mouse x
    this.setState({dragTarget: e.target.dataset.name, dragStartX: e.clientX});
    e.preventDefault();
  };

  // cell rendering by multigrid
  _cellRenderer = ({ columnIndex, key, rowIndex, style }: Object) => {
    let colname = this.props.columnVisible[columnIndex];

    // row 0: select all and header row
    if (rowIndex == 0) {
      if (columnIndex==0) {
        let allselected = this.props.rowsSelected.size == this.props.data.length
        return (
          <div className={"cell"} key={key} style={style}>
            <input type="checkbox" checked={allselected} onChange={this.props.onRowSelectToggleAll} />
          </div>
        )
      } else { // header row
        return (
          <div className={"headers"} key={key} style={style}>
            <div className={"headerTop"}>
              <div className={"headerTopTitle"}>{colname}</div>
              <Glyphicon className={"headerTopSort"} glyph="sort" data-name={colname} onClick={this.props.doSort} />
              <div className="headerTopResize" data-name={colname} onMouseDown={this._columnDrag} />
            </div>
            <div className={"headerBottom"}>
              <input className="headerBottomText" data-name={colname} onChange={this.props.doSearch} value={this.props.columnSearch[colname]} placeholder={"search " + colname} type="text"/>
              <input className="headerBottomCheck" data-name={colname} type="checkbox" onChange={this.props.doFilter} checked={this.props.columnFilter.has(colname)} title="Check this for filter instead of search"/>
            </div>
          </div>
        )
      }
    }

    let cn = "cell";

    if ((rowIndex % 2) == 1) {
      cn += " odd-row"
    }
    let id = this.props.data[rowIndex-1][0].toString()
    let selected = this.props.rowsSelected.has(id)
    if (selected) {
      cn += " selected-row"
    }
    if (this.props.searchCursor == id) {
      cn += " found-select-row"
    } else if (this.props.rowsFoundSorted.includes(id)) {
      cn += " found"
    }

    // column 0: select column
    if (columnIndex==0) {
      return (
        <div className={cn} key={key} style={style}>
          <input type="checkbox" checked={selected} name={id} onChange={this.props.onRowSelectChange} />
        </div>
      )
    }

    let tcolumnIndex = window.columns.indexOf(colname)
    let val = this.props.data[rowIndex-1][tcolumnIndex]

    // column 1: fixed name column
    if (columnIndex==1) {
      return (
        <div
          className={cn}
          key={key}
          style={style}
          > {val}
        </div>
      )
    }

    // is cell selected? And/or active?
    if (columnIndex === this.state.cursorColumn && rowIndex === this.state.cursorRow) {
        cn += " selected"
    }

    // check if file column
    if (colname.toLowerCase().includes("file")) {
      val = <a href={"/downloads/" + val}>{val.slice(val.lastIndexOf("/")+1)}</a>
    }

    return (
      <div
        className={cn}
        key={key}
        //onClick={() => this._selectCell({ cursorColumn: columnIndex, cursorRow: rowIndex, scrollToColumn: columnIndex, scrollToRow: rowIndex })}
        style={style}
        > {val}
      </div>
    )
  };

  // used by multigrid and keyboard nav func to move selector around
  _selectCell = ({ cursorColumn = this.state.cursorColumn, cursorRow = this.state.cursorRow, scrollToColumn = this.state.cursorColumn, scrollToRow = this.state.cursorRow }: Object = {}) => {
    if ((cursorColumn>1) && (cursorRow >0)) {
      this.setState({ scrollToColumn, scrollToRow, cursorColumn, cursorRow, editActive: false })
      if (this.aks) {
        this.aks.focus()
      } else {
        console.log("Error: AKS not found.")
      }
    }
  };

  _getColumnWidth = ({index} : Object) => {
    if (index>0) {
      return this.props.columnWidths[this.props.columnVisible[index]]
    } else {
      return 50
    }
  };

  _onKeyDown = (e: SyntheticKeyboardEvent<HTMLDivElement>) => {
    if (!this.state.editActive && e.target.className != 'headerBottomText') { // headerBottomText is the searchFields and we want regular arrow function in those
      switch (e.key) {
        case 'ArrowLeft':
          this._selectCell({scrollToColumn: this.state.cursorColumn - 1, cursorColumn: this.state.cursorColumn - 1})
          break;
        case 'ArrowRight':
          this._selectCell({scrollToColumn: this.state.cursorColumn + 1, cursorColumn: this.state.cursorColumn + 1})
          break;
        case 'ArrowUp':
          this._selectCell({scrollToRow: this.state.cursorRow - 1, cursorRow: this.state.cursorRow - 1})
          break;
        case 'ArrowDown':
          this._selectCell({scrollToRow: this.state.cursorRow + 1, cursorRow: this.state.cursorRow + 1})
          break;
      }
    }
  }

  render () {
    const {scrollToColumn, scrollToRow, dragCurrentX} = this.state;
    const csms = {left: dragCurrentX, position: "fixed", height: "50px", borderStyle: "dashed", borderWidth: "3px", zIndex: "3"};
    return (
      <div
        id="aks"
        tabIndex={1}
        ref={this._setaks}
        onKeyDown={this._onKeyDown}>

        <AutoSizer>
          {({height, width}) => (
            <MultiGrid
              // react
              ref={this._setMugi}
              // poorly documented (or documented in Grid)
              cellRenderer={this._cellRenderer}
              columnCount={this.props.columnVisible.length}
              rowCount={this.props.data.length+1}
              scrollToColumn={scrollToColumn}
              scrollToRow={scrollToRow}
              rowHeight={50}
              height={height}
              width={width}
              columnWidth={this._getColumnWidth}
              overscanRowCount={0}
              //// documented
              fixedColumnCount={2}
              fixedRowCount={1}
              styleTopLeftGrid={stlg}
              styleTopRightGrid={strg}
              styleBottomLeftGrid={sblg}
            />)}
        </AutoSizer>
        <div id="columnSizeMarker" style={csms}/>
      </div>
    )
  }
}
