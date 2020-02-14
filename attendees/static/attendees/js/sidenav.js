class SideNavUI {
  constructor() {
    this.sideNav = document.querySelector('#side-nav');
    this.mainSideNav = document.querySelector('.main-side-nav');
    this.mainNav = document.querySelector('#main-nav');
    this.mainFeed = document.querySelector('#main-feed');
    this.mainFooter = document.querySelector('#main-footer');
  }

  hideSideNav() {
    this.sideNav.classList.add('hide');
    this.mainSideNav.classList.add('hide');
    this.mainNav.classList.add('wide');
    this.mainFeed.classList.add('wide');
    this.mainFooter.classList.add('wide');
  }

  showSideNav() {
    this.sideNav.classList.remove('hide');
    this.mainSideNav.classList.remove('hide');
    this.mainNav.classList.remove('wide');
    this.mainFeed.classList.remove('wide');
    this.mainFooter.classList.remove('wide');
  }
}


// APP CONTROL
sideNavUI = new SideNavUI();

// EVENT LISTENERS

// Sidebar Toggle
document.querySelector('.nav-toggler').addEventListener('click', toggleSideNav);


// Sidebar Toggle
function toggleSideNav() {
  if(sideNavUI.sideNav.classList.contains('hide')) {
    sideNavUI.showSideNav();
  } else {
    sideNavUI.hideSideNav();
  }
}