
var elems= document.querySelectorAll('input[type="submit"]');
//document.addEventListener('submit', function () {})

elems.forEach(function(btn) {
    // Вешаем событие клик
    
    btn.addEventListener('click', function(e) {
        btn.hidden = true;
        sleep(2000).then(() => { btn.hidden = false; });
       
    })
  })
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


