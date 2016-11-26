
function edgeClicked(gameboard){
}

$.widget( "custom.gameboard", {
    // default options
    options: {
    },

    poll_freq : 1000,

    _create: function() {
        this.move_store = [];
        console.log(this.options);

        this.board_holder = $("<h2></h2>").appendTo(this.element);
        this.game_holder = $("<div></div>").appendTo(this.element);

        this.current_player = this.options.current_player;
        this.num_players = this.options.num_players;
        this.this_player = this.options.player_id;

        this.game_id = this.options.game_id;

        this.width = this.options.width;
        this.height = this.options.height;

        this.buildTurnCounter();
        this.buildBoard();

        this.options.nodes.forEach(function(n){
            this._edgeClicked(n[0],n[1],n[2]);
        }.bind(this));

        this.updateBoard();

        this.poll_timer = setInterval(function(){
            this.pollMoves();
        }.bind(this), this.poll_freq);

        this.polling = !this._myTurn();


        console.log(this.num_players);
        if(this.num_players <= 1){
            this.polling = true;
            this.element.hide();
        }
    },


    pollMoves: function() {
        if(this.polling){
            $.ajax('/games/' + this.game_id + '/poll').done(function(data){
                if(this.polling){
                    this.updated(data.game_data);
                }
            }.bind(this));
        }
    },


    updated: function(game_data){
        if( game_data.nodes.length > this.move_store.length){
            for(var i = this.move_store.length; i < game_data.nodes.length; i++){
                var n = game_data.nodes[i];
                this._edgeClicked(n[0],n[1],n[2]);
            }
        }


        if(game_data.num_players != this.num_players){
            this.num_players = game_data.num_players;
            this.buildTurnCounter();
            this.element.show();

        }

    },


    buildTurnCounter:function() {
        this.game_holder.html('');
        this.game_holder.addClass('player_holders');
        this.player_holders = [];

        for(var i = 0; i < this.num_players; i++){
            var player_screen = $("<div></div>").appendTo(this.game_holder);
            player_screen.addClass('player' + i).addClass('player');
            this.player_holders.push(player_screen);

            if(i == this.this_player){
                player_screen.addClass('current');
            }
        }

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


            var skip = false;
            if(dir === 0){
                skip = skip || this._markCell(row, col);
                skip = skip || this._markCell(row-1, col);
            }else{
                skip = skip || this._markCell(row, col);
                skip = skip || this._markCell(row, col-1);
            }

            this._sendEdgeMove(row, col, dir);

            this.move_store.push([row, col, dir]);

            if(!skip){
                this._nextPlayer();
            }
        }
    },

    _sendEdgeMove: function(row, col, dir){
        var url = "/games/" + this.game_id ;


        var data = {
            row: row,
            col: col,
            dir: dir,
            player: this.current_player
        };

        $.ajax(url,{
            data:data
        });
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
            if(self._myTurn()){
                self._edgeClicked(rowid, colid, dir);
            }
        });
    },

    _markCell: function(row, col){
        if(this._checkCell(row, col)){
            this.cells[row][col].addClass('taken').addClass('player' + this.current_player);
            return true;
        }
        return false;
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

    _nextPlayer: function(){
        console.log(this.player_holders);
        this.player_holders[this.current_player].removeClass('active');
        this.current_player = (this.current_player + 1) % this.num_players
        this.updateBoard();

        this.polling = !this._myTurn();

    },


    updateBoard:function(){

        this.player_holders[this.current_player].addClass('active');
        this.element.toggleClass('active', this._myTurn());

        if(this._myTurn()){
            this.board_holder.html('It is your turn');
        }else{

            this.board_holder.html('It is player ' + this.current_player + ' turn');
        }
    },

    _myTurn: function(){
        return this.current_player == this.this_player;
    },



});
