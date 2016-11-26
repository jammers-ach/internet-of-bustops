
function edgeClicked(gameboard){
}

$.widget( "custom.gameboard", {
    // default options
    options: {

    },

    _create: function() {
        console.log(this.options);
        this.width = this.options.width;
        this.height = this.options.height;

        this.buildBoard();

        //this.options.nodes.forEach(function(n){
            //this._edgeClicked(n[0],n[1],n[2]);
        //}.bind(this));
    },


    buildBoard:function() {
        this.edges = {};
        this.cells = {};

        for(var x =0; x < this.height;x++){
            this.edges[x] = {};
            this.cells[x] = {};
            for(var y =0; y < this.height;y++){
                this.edges[x][y] = {0:null, 1:null}; //1 is up, 0 is left
                this.cells[x][y] = null;
            }
        }

        this.element.html();
        this.element.addClass('board');
        this.table = $('<table></table>').appendTo(this.element);

        for(var i = 0;i < this.height - 1;i++){
            // Bulild an edge row
            this._buildEdgeRow(i);
            this._buildCellRow(i);
        }
        this._buildEdgeRow(this.height-1);
    },

    _buildCellRow: function(row_index){
        var row = $("<tr></tr>").addClass('cellrow');
        row.attr('data-rowid', row_index);
        row.appendTo(this.table);

        for(var i = 0;i < this.width;i++){
            var cell_cell = $('<td></td>').addClass('cell');
            var edge_cell = $('<td></td>').addClass('edge');

            edge_cell.attr('data-colid', i);
            edge_cell.attr('data-dir', 1);

            this.edges[row_index][i][1] = edge_cell;


            row.append(edge_cell);
            this.bindClick(edge_cell);
            if(i < this.width-1){
                row.append(cell_cell);
                this.cells[row_index][i] = cell_cell;
            }
        }
    },

    _buildEdgeRow: function(row_index){
        var row = $("<tr></tr>").addClass('edgerow');
        row.attr('data-rowid', row_index);
        row.appendTo(this.table);

        for(var i = 0; i < this.width; i++){
            var node_cell = $('<td></td>').addClass('node');
            var edge_cell = $('<td></td>').addClass('edge');

            edge_cell.attr('data-colid', i);
            edge_cell.attr('data-dir', 0);

            this.edges[row_index][i][0] = edge_cell;

            row.append(node_cell);
            if(i < this.width-1){
                row.append(edge_cell);
                this.bindClick(edge_cell);
            }
        }
    },

    _edgeClicked: function(row, col, dir){
        var edge = this.edges[row][col][dir];
        if(!this._isTaken(row, col, dir)){
            edge.addClass('taken');


            if(dir === 0){
                this._markCell(row, col);
                this._markCell(row-1, col);
            }else{
                this._markCell(row, col);
                this._markCell(row, col-1);
            }
        }
    },


    bindClick: function(edge){
        var self = this;

        edge.click(function(){
            var rowid = $(this).closest('tr').attr('data-rowid');
            var colid = $(this).attr('data-colid');
            var dir = $(this).attr('data-dir');

            rowid = parseInt(rowid);
            colid = parseInt(colid);
            dir = parseInt(dir);
            self._edgeClicked(rowid, colid, dir);
        });
    },

    _markCell: function(row, col){
        if(this._checkCell(row, col)){
            this.cells[row][col].addClass('taken').addClass('a');
        }
    },

    /**
     * Checks to see if a box should be taken or not
     */
    _checkCell: function(row, col){

        if(col == this.width - 1 || col < 0){
            return;
        }
        if(row == this.height - 1 || row < 0){
            return;
        }
        return this._isTaken(row, col, 0) &
            this._isTaken(row, col, 1) &
            this._isTaken(row , col +1, 1) &
            this._isTaken(row +1, col , 0);
    },

    _isTaken: function(row, col, dir){
        var edge = this.edges[row][col][dir];
        edge.addClass('checked');

        setTimeout(function(){
            edge.removeClass('checked');
        }, 200);

        return edge.hasClass('taken');
    },

});
