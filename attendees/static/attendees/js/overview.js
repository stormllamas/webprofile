class OverviewUI {
  constructor() {
    this.tpe = document.querySelector('.tpe');
    this.tpr = document.querySelector('.tpr');
    this.tpb = document.querySelector('.tpb');
  }

  showtpe() {
    this.tpe.classList.add('show');
  }
  
  hidetpe() {
    this.tpe.classList.remove('show');
  }
  
  showtpr() {
    this.tpr.classList.add('show');
  }
  
  hidetpr() {
    this.tpr.classList.remove('show');
  }
  
  showtpb() {
    this.tpb.classList.add('show');
  }
  
  hidetpb() {
    this.tpb.classList.remove('show');
  }
}


// APP CONTROL
overviewUI = new OverviewUI();

// EVENT LISTENERS

// Points Hover
document.getElementById('points-earned').addEventListener('mouseenter', showtpe);
document.getElementById('points-earned').addEventListener('mouseleave', hidetpe);
document.getElementById('points-redeemed').addEventListener('mouseenter', showtpr);
document.getElementById('points-redeemed').addEventListener('mouseleave', hidetpr);
document.getElementById('points-balance').addEventListener('mouseenter', showtpb);
document.getElementById('points-balance').addEventListener('mouseleave', hidetpb);


// Points Hover
function showtpe() {
  overviewUI.showtpe();
}

function hidetpe() {
  overviewUI.hidetpe();
}

function showtpr() {
  overviewUI.showtpr();
}

function hidetpr() {
  overviewUI.hidetpr();
}

function showtpb() {
  overviewUI.showtpb();
}

function hidetpb() {
  overviewUI.hidetpb();
}