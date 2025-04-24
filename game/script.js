let randomNumber = Math.floor(Math.random() * 100) + 1;
let attempts = 0;

document.getElementById('submit').addEventListener('click', function() {
    const userGuess = parseInt(document.getElementById('guess').value);
    const result = document.getElementById('result');
    
    attempts++;

    if (userGuess === randomNumber) {
        result.textContent = `Поздравляю! Вы угадали число ${randomNumber} за ${attempts} попыток!`;
        document.getElementById('restart').style.display = 'block';
    } else if (userGuess < randomNumber) {
        result.textContent = 'Слишком низко! Попробуйте снова.';
    } else {
        result.textContent = 'Слишком высоко! Попробуйте снова.';
    }
});

document.getElementById('restart').addEventListener('click', function() {
    randomNumber = Math.floor(Math.random() * 100) + 1;
    attempts = 0;
    document.getElementById('result').textContent = '';
    document.getElementById('guess').value = '';
    document.getElementById('restart').style.display = 'none';
});
