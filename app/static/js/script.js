function width() {
  return (outerWidth > innerWidth && innerWidth) || outerWidth;
}

function show_team_members() {
  let max_members = Math.floor((width() - 250) / 240);
  if (max_members < 1) max_members = 1; // this is how many members should be visible
  if (max_members >= members.length) {
    document.getElementById("team_arrow_right").style.opacity = "0";
    document.getElementById("team_arrow_left").style.opacity = "0";
  } else {
    document.getElementById("team_arrow_right").style.opacity = "1";
    document.getElementById("team_arrow_left").style.opacity = "1";
  }
  if (members[members.length - 1][1]) {
    document.getElementById("team_arrow_left").style.opacity = "0";
  } else {
    document.getElementById("team_arrow_left").style.opacity = "1";
  }
  if (members[0][1]) {
    document.getElementById("team_arrow_left").style.opacity = "0";
  } else {
    document.getElementById("team_arrow_left").style.opacity = "1";
  }

  let visible = 0;
  let first_member = 0;
  for (let i = 0; i < members.length * 2; i++) {
    if (visible == 0 && members[i % members.length][1]) {
      first_member = i % members.length;
      visible += 1;
      members[i % members.length][0].style.display = "block";
    } else if (visible > 0 && max_members > visible) {
      members[i % members.length][1] = true;
      visible += 1;
      members[i % members.length][0].style.display = "block";
    } else if (max_members >= visible && i % members.length != first_member) {
      members[i % members.length][1] = false;
      members[i % members.length][0].style.display = "none";
    } else if (visible > 0 && i % members.length == first_member) {
      return;
    }
  }
}

members = [];

window.addEventListener("resize", show_team_members);

async function team_left() {
  let max_members = Math.floor((width() - 250) / 240);
  if (members[0][1] == false) {
    document.getElementById("team_arrow_right").style.opacity = "1";
    for (let i = 0; i < members.length; i++) {
      if (max_members > 1 && members[i][1] && (i + 1 >= members.length || members[i + 1][1] == false)) {
        members[i][0].style.transition = "0.4s";
        members[i][0].style.transform = "scale(0)";
        await sleep(200);
        members[i][0].style.transition = "";
        members[i][0].style.transform = "";
        members[i][1] = false;
        members[i][0].style.display = "none";
        break;
      } else if (max_members <= 1 && members[i][1] && (i + 1 >= members.length || members[i + 1][1] == false)) {
        members[i][0].style.transition = "0.4s";
        members[i][0].style.transform = "scale(0)";
        await sleep(200);
        members[i][0].style.transition = "";
        members[i][0].style.transform = "";
        members[i][1] = false;
        members[i][0].style.display = "none";
        
        members[i-1][1] = true;
        members[i-1][0].style.display = "block";
        members[i-1][0].style.width = "";
        
        if (members[0][1]) {
          document.getElementById("team_arrow_left").style.opacity = "0";
        }
        return;
      }
    }
    for (let i = 0; i < members.length; i++) {
      if (members[i + 1][1]) {
        members[i][1] = true;
        members[i][0].style.display = "block";
        members[i][0].style.width = "";
        break;
      }
    }
    if (members[0][1]) {
      document.getElementById("team_arrow_left").style.opacity = "0";
    }
  }
}

async function team_right() {
  let max_members = Math.floor((width() - 250) / 240);
  if (members[members.length - 1][1] == false) {
    document.getElementById("team_arrow_left").style.opacity = "1";
    for (let i = 0; i < members.length; i++) {
      if (members[i][1] && max_members > 1) {
        members[i][0].style.transition = "0.4s";
        members[i][0].style.transform = "scale(0)";
        await sleep(200);
        members[i][0].style.transition = "";
        members[i][0].style.transform = "";
        members[i][1] = false;
        members[i][0].style.display = "none";
        break;
      } else if (members[i][1] && max_members <= 1) {
        members[i][0].style.transition = "0.4s";
        members[i][0].style.transform = "scale(0)";
        await sleep(200);
        members[i][0].style.transition = "";
        members[i][0].style.transform = "";
        members[i][1] = false;
        members[i][0].style.display = "none";
        
        members[i+1][1] = true;
        members[i+1][0].style.display = "block";
        members[i+1][0].style.width = "";
        
        if (members[members.length - 1][1]) {
          document.getElementById("team_arrow_right").style.opacity = "0";
        }
        return
      }
    }
    for (let i = members.length - 1; i > 0; i--) {
      if (members[i - 1][1] && members[i][1] == false) {
        members[i][1] = true;
        members[i][0].style.display = "block";
        members[i][0].style.width = "";
        break;
      }
    }
    if (members[members.length - 1][1]) {
    document.getElementById("team_arrow_right").style.opacity = "0";
    }
  }
}


function sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}
