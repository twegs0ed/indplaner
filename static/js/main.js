
var elems= document.querySelectorAll('input[type="submit"]');
//document.addEventListener('submit', function () {})

elems.forEach(function(btn) {
    // Вешаем событие клик
    
    btn.addEventListener('click', function(e) {
      elems.forEach(function(btn) {
        btn.hidden = true;
        sleep(2000).then(() => { btn.hidden = false; });
      })
    })
  })
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  function copyToClipboard(txt) {
    const textArea = document.createElement("textarea");
    textArea.value = txt;
    document.body.appendChild(textArea);
    textArea.focus({preventScroll: true})
    textArea.select();
    try {
       document.execCommand('copy');
    } catch (err) {
       console.error('Unable to copy to clipboard', err);
    }
    document.body.removeChild(textArea);


/*
    navigator.clipboard.writeText(txt).then(() => {
      console.log('Content copied to clipboard');
    },() => {
      console.error('Failed to copy');
    });*/
  
  }


