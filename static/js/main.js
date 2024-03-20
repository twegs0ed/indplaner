
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
    navigator.clipboard.writeText(txt).then(() => {
      console.log('Content copied to clipboard');
      /* Resolved - text copied to clipboard successfully */
    },() => {
      console.error('Failed to copy');
      /* Rejected - text failed to copy to the clipboard */
    });
  
  }


