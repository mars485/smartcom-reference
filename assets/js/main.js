const menu=document.querySelector('.menu-toggle');const links=document.querySelector('.nav-links');if(menu&&links){menu.addEventListener('click',()=>{const opened=links.classList.toggle('open');menu.setAttribute('aria-expanded',String(opened));});links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{links.classList.remove('open');menu.setAttribute('aria-expanded','false');}));}

const leadForm=document.querySelector('#lead-form');if(leadForm){leadForm.addEventListener('submit',e=>{e.preventDefault();const status=document.querySelector('#form-status');status.textContent='✓ Форма заполнена корректно. Это демонстрация: данные не отправлены.';leadForm.reset();});}

// Close the mobile menu with Escape or when clicking outside it.
if(menu&&links){document.addEventListener('keydown',event=>{if(event.key==='Escape'){links.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus();}});document.addEventListener('click',event=>{if(!event.target.closest('nav')){links.classList.remove('open');menu.setAttribute('aria-expanded','false');}});}
