//@flow
"use strict";

import React from 'react'
import {Button, ButtonGroup, ButtonToolbar, Glyphicon} from 'react-bootstrap'
import SearchControl from './searchControl'

type Props = {
  rowsSelected: Set<string>,
  rowsFoundSorted: Array<string>,
  columnFilter: Set<string>,
  setSearchHighlight: Function,
  clearSearch: Function,
  doFilterClear: Function,
  doSelectFound: Function,
  scrollToExtreme: Function
}

export default class ControlRow extends React.PureComponent<Props> {
  render() {
    const noneselected = this.props.rowsSelected.size==0  // track whether buttons which deal with selection should be enabled

    return (
      <div id="toolbar">
        <div id="toolbarleft">
          <SearchControl scrollToExtreme={this.props.scrollToExtreme} rowsFoundSorted={this.props.rowsFoundSorted} columnFilter={this.props.columnFilter} setSearchHighlight={this.props.setSearchHighlight} doFilterClear={this.props.doFilterClear} doSearchClear={this.props.clearSearch} doSelectFound={this.props.doSelectFound} />
        </div>
        <div id="toolbarright">
          <ButtonToolbar>
            <ButtonGroup>
              <Button bsSize="sm" bsStyle="primary" onClick={() => window.location.href = window.location.href + "exportexcel/"}>Download table <Glyphicon glyph="cloud-download" /></Button>
              <Button bsSize="sm" bsStyle="primary" disabled={noneselected} onClick={() => window.location.href = window.location.href + "exportexcel/" + Array.from(this.props.rowsSelected).join(",")}>Download selected <Glyphicon glyph="cloud-download" /></Button>
            </ButtonGroup>
          </ButtonToolbar>
        </div>
      </div>
    )
  }
}
