const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


  // -webkit-box-shadow: 0 1px 4px 0 rgba(0,0,0,0.05), 0 5px 30px 0 rgba(0,0,0,0.05);
  // box-shadow: 0 1px 4px 0 rgba(0,0,0,0.05), 0 5px 30px 0 rgba(0,0,0,0.05);
// Navbar Changer
window.addEventListener('scroll', function() {
  if (window.scrollY > 0) {
    document.querySelector('#main-nav').style.boxShadow = '0 1px 4px 0 rgba(0,0,0,0.05), 0 5px 30px 0 rgba(0,0,0,0.05)';
    
  } else {
    document.querySelector('#main-nav').style.boxShadow = '';
  }
});