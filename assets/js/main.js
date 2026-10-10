const menu = document.querySelector('.menu-toggle');
const links = document.querySelector('.nav-links');
function closeMenu(restoreFocus = false) {
  if (!menu || !links) return;
  links.classList.remove('open');
  menu.setAttribute('aria-expanded', 'false');
  menu.setAttribute('aria-label', 'Открыть меню');
  if (restoreFocus) menu.focus();
}
if (menu && links) {
  menu.addEventListener('click', () => {
    const opened = links.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(opened));
    menu.setAttribute('aria-label', opened ? 'Закрыть меню' : 'Открыть меню');
  });
  links.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && links.classList.contains('open')) closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('nav')) closeMenu();
  });
  window.matchMedia('(min-width: 701px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
  });
}

const leadForm = document.querySelector('#lead-form');
if (leadForm) {
  leadForm.addEventListener('submit', event => {
    event.preventDefault();
    const status = document.querySelector('#form-status');
    status.textContent = 'Поля заполнены корректно. Это демонстрация: данные не отправлены и не сохранены.';
  });
}
