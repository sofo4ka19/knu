document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const startButton = document.getElementById('start-game');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const initialValueInput = document.getElementById('initial-value');
    const operationSelect = document.getElementById('operation');
    const currentScoreDisplay = document.getElementById('current-score');
    const highScoreDisplay = document.getElementById('high-score');
    const details = document.getElementById('overlay');

    let board = [];
    let boardWidth = 4;
    let boardHeight = 4;
    let initialValue = 2;
    let operation = 'addition';
    let score = 0;
    let highScore = parseInt(localStorage.getItem('highScore')) || 0;
    let startTime;

    highScoreDisplay.textContent = highScore;

    startButton.addEventListener('click', startGame);

    function startGame() {
        boardWidth = parseInt(widthInput.value);
        boardHeight = parseInt(heightInput.value);
        initialValue = parseInt(initialValueInput.value);
        operation = operationSelect.value;
        resetBoard();
        score = 0;
        currentScoreDisplay.textContent = score;
        generateTile();
        generateTile();
        drawBoard();
        document.addEventListener('keydown', handleInput);
        startTime=Date.now();
    }

    function resetBoard() {
        board = Array.from({ length: boardHeight }, () => Array(boardWidth).fill(0));
    }

    function generateTile() {
        let emptyTiles = [];
        for (let y = 0; y < boardHeight; y++) {
            for (let x = 0; x < boardWidth; x++) {
                if (board[y][x] === 0) {
                    emptyTiles.push({ x, y });
                }
            }
        }
        if (emptyTiles.length > 0) {
            let { x, y } = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            board[y][x] = initialValue;
        }
    }
    function generateTileColor(tile, value) {
         let color = {
            red: 255,
            green: 225,
            blue: 225
         };
        let i = initialValue;
        while(i<=value){
            if(color.green>5 & color.blue>5){
                color.green-=10;
                color.blue-=10;
            }
            else{
                color.red = Math.floor(Math.random*250+5);
                color.blue = Math.floor(Math.random*250+5);
                color.green = Math.floor(Math.random*250+5);
            }
            (operation=="addition")?(i*=2):(i*=i);
        }
        return `rgb(${color.red}, ${color.green}, ${color.blue})`;

    }

    function drawBoard() {
        gameBoard.innerHTML = '';
        gameBoard.style.gridTemplateColumns = `repeat(${boardWidth}, 100px)`;
        board.forEach(row => {
            row.forEach(value => {
                const tile = document.createElement('div');
                tile.classList.add('tile');
                if (value > 0) {
                    tile.textContent = value;
                    tile.style.backgroundColor=generateTileColor(tile, value);
                }
                gameBoard.appendChild(tile);
            });
        });
    }

    function handleInput(e) {
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
            e.preventDefault();
            let moved = false;
            switch (e.key) {
                case 'ArrowUp': moved = move('up'); break;
                case 'ArrowDown': moved = move('down'); break;
                case 'ArrowLeft': moved = move('left'); break;
                case 'ArrowRight': moved = move('right'); break;
            }
            if (moved) {
                generateTile();
                drawBoard();
                updateHighScore();
                if (checkGameOver()) {
                    alert('Game Over!');
                    document.removeEventListener('keydown', handleInput);
                }
            }
        }
    }

    function move(direction) {
        let moved = false;

        const combine = (a, b) => {
            const result = operation === 'addition' ? a + b : a * b;
            score += result;
            currentScoreDisplay.textContent = score;
            return result;
        };

        const slide = (rowOrCol) => {
            let arr = rowOrCol.filter(val => val);
            let missing = rowOrCol.length - arr.length;
            let zeros = Array(missing).fill(0);
            return arr.concat(zeros);
        };

        const merge = (rowOrCol) => {
            for (let i = 0; i < rowOrCol.length - 1; i++) {
                if (rowOrCol[i] && rowOrCol[i] === rowOrCol[i + 1]) {
                    rowOrCol[i] = combine(rowOrCol[i], rowOrCol[i + 1]);
                    rowOrCol[i + 1] = 0;
                }
            }
            return rowOrCol;
        };

        const operate = (array) => {
            let oldArray = array.slice();
            let newArray = slide(merge(slide(array)));
            return { moved: !arraysEqual(oldArray, newArray), newArray };
        };

        const arraysEqual = (a, b) => {
            return JSON.stringify(a) === JSON.stringify(b);
        };

        if (direction === 'left' || direction === 'right') {
            for (let y = 0; y < boardHeight; y++) {
                let row = board[y];
                if (direction === 'right') row = row.reverse();
                let { moved: rowMoved, newArray } = operate(row);
                if (direction === 'right') newArray = newArray.reverse();
                board[y] = newArray;
                if (rowMoved) moved = true;
            }
        } else if (direction === 'up' || direction === 'down') {
            for (let x = 0; x < boardWidth; x++) {
                let col = board.map(row => row[x]);
                if (direction === 'down') col = col.reverse();
                let { moved: colMoved, newArray } = operate(col);
                if (direction === 'down') newArray = newArray.reverse();
                newArray.forEach((val, y) => board[y][x] = val);
                if (colMoved) moved = true;
            }
        }

        return moved;
    }

    function updateHighScore() {
        if (score > highScore) {
            highScore = score;
            localStorage.setItem('highScore', highScore);
            localStorage.setItem('highScoreBoardWidth', boardWidth);
            localStorage.setItem('highScoreBoardHeight', boardHeight);
            localStorage.setItem('highScoreValue', initialValue);
            localStorage.setItem('highScoreOperation', operation);
            localStorage.setItem('highScoreStartTime', startTime);
            localStorage.setItem('highScoreEndTime', Date.now());
            localStorage.setItem('highScoreDuration', (Date.now()-startTime)/1000);
            highScoreDisplay.textContent = highScore;
        }
    }
    function getTimeTaken(){
        let highScoreDuration = parseInt(localStorage.getItem('highScoreDuration'))
        let hours = Math.floor(highScoreDuration/3600);
        let minutes = Math.floor(highScoreDuration/60) - hours*60;
        let seconds = highScoreDuration - hours*3600 - minutes*60;
        if(hours!=0){
            return `${hours} hours ${minutes} minutes ${seconds} seconds`;
        }
        else if(minutes!=0){
            return `${minutes} minutes ${seconds} seconds`;
        }
        else{
            return `${seconds} seconds`;
        }
    }
    const moreButton = document.getElementById('more-info');
    moreButton.addEventListener('click', showSettings);

    function showSettings() {
        let highScoreStartTime = parseInt(localStorage.getItem('highScoreStartTime'));
        let highScoreEndTime = parseInt(localStorage.getItem('highScoreEndTime'));
        const settingsPopup = document.createElement('div');
        settingsPopup.classList.add('settings-popup');
        settingsPopup.innerHTML = `
            <h2>Settings Used for High Score</h2>
            <p>Board Size: ${localStorage.getItem('highScoreBoardWidth')}x${localStorage.getItem('highScoreBoardHeight')}</p>
            <p>Initial Value: ${localStorage.getItem('highScoreValue')}</p>
            <p>Operation: ${localStorage.getItem('highScoreOperation')}</p>
            <p>Start time: ${new Date(highScoreStartTime).getDate()}.${new Date(highScoreStartTime).getMonth()+1}.${new Date(highScoreStartTime).getFullYear()} ${new Date(highScoreStartTime).getHours()}:${new Date(highScoreStartTime).getMinutes()}:${new Date(highScoreStartTime).getSeconds()}</p>
            <p>End time: ${new Date(highScoreEndTime).getDate()}.${new Date(highScoreEndTime).getMonth()+1}.${new Date(highScoreEndTime).getFullYear()} ${new Date(highScoreEndTime).getHours()}:${new Date(highScoreEndTime).getMinutes()}:${new Date(highScoreEndTime).getSeconds()}</p>
            <p>Time Taken: ${getTimeTaken()}</p>
            <button id="close-popup">Close</button>
        `;
        details.appendChild(settingsPopup);
        details.style.display="flex";
        document.body.style.overflow="hidden";

        const closeButton = settingsPopup.querySelector('#close-popup');
        closeButton.addEventListener('click', () => {
            details.style.display="none";
            document.body.style.overflow="";
            settingsPopup.remove();
        });
    }

    function checkGameOver() {
        for (let y = 0; y < boardHeight; y++) {
            for (let x = 0; x < boardWidth; x++) {
                if (board[y][x] === 0) return false;
                if (x < boardWidth - 1 && board[y][x] === board[y][x + 1]) return false;
                if (y < boardHeight - 1 && board[y][x] === board[y + 1][x]) return false;
            }
        }
        return true;
    }
});
