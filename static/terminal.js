const main = document.querySelector('#main-container');
let input = document.querySelector('#Input');

function typeEffect(element, text, speed = 15, callback) {
  let i = 0;
  function typing() {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(typing, speed);
    } else if (callback) callback();
  }
  typing();
}

function perform_command(e) {
  if (e.key === 'Enter') {
    const command = input.value.trim();
    const cmdLine = document.createElement('div');
    cmdLine.innerHTML = `<span class='prompt'>.\\Quinix\\> </span>${command}`;
    main.appendChild(cmdLine);

    fetch('/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command })
    })
      .then(res => res.json())
      .then(data => {
        if (data.output === "__clear__") {
          main.innerHTML = "";
          newPromptLine();
          return;
        }

        const output = document.createElement('div');
        output.className = 'output';
        main.appendChild(output);
        typeEffect(output, "\n" + data.output, 10, () => {
          main.appendChild(document.createElement('br'));
          newPromptLine();
        });
        main.scrollTop = main.scrollHeight;
      });

    input.disabled = true;
    input.removeEventListener('keydown', perform_command);
     if (command === 'exit') {
      setTimeout(() => {
        window.close(); // will close the browser tab if allowed
      }, 1500);
      return;
    }
  }
 
}

function newPromptLine() {
  const prompt = document.createElement('span');
  prompt.className = 'prompt';
  prompt.innerText = '.\\Quinix\\> ';

  const newInput = document.createElement('input');
  newInput.className = 'same-font';
  newInput.id = 'Input';
  newInput.setAttribute('autofocus', 'autofocus');

  main.appendChild(prompt);
  main.appendChild(newInput);
  input = newInput;
  input.addEventListener('keydown', perform_command);
}

input.addEventListener('keydown', perform_command);
