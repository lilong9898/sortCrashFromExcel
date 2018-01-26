    function onClickToToggleCrashDivVisibilityById(button, crashDivId, anchorLinkId){

        visibility = button.getAttribute("visibility");
        visibleInnerHTML = button.getAttribute("visibleInnerHTML");
        invisibleInnerHTML = button.getAttribute("invisibleInnerHTML");

        crashDiv = document.getElementById(crashDivId);
        anchorLink = document.getElementById(anchorLinkId);

        // 隐藏
        if(visibility == "visible"){
            crashDiv.setAttribute("hidden", "hidden");
            button.setAttribute("visibility", "invisible");
            button.innerHTML = invisibleInnerHTML;
            anchorLink.style="color:bluefont-weight;font-weight:normal";
        }
        // 显示
        else if(visibility == "invisible"){
            crashDiv.removeAttribute("hidden");
            button.setAttribute("visibility", "visible");
            button.innerHTML = visibleInnerHTML;
            anchorLink.style="color:bluefont-weight;font-weight:bold";
        }
    }

    function onClickToToggleElementsVisibilityByClassName(button, className){

        visibility = button.getAttribute("visibility");
        visibleInnerHTML = button.getAttribute("visibleInnerHTML");
        invisibleInnerHTML = button.getAttribute("invisibleInnerHTML");

        elements = document.getElementsByClassName(className);

        // 隐藏
        if(visibility == "visible"){
            var i;
            for(i = 0; i < elements.length; i++){
                elements[i].setAttribute("hidden", "hidden");
            }
            button.setAttribute("visibility", "invisible");
            button.innerHTML = invisibleInnerHTML;
        }
        // 显示
        else{
            var i;
            for(i = 0; i < elements.length; i++){
                elements[i].removeAttribute("hidden");
            }
            button.setAttribute("visibility", "visible");
            button.innerHTML = visibleInnerHTML;
        }

    }

function onVersionNameCheckBoxClicked(checkBox){
    for(i = 1; i < arguments.length; i++){
        strCrashOrder = arguments[i];
        buttonToggleCrashVisibility = document.getElementById("button_" + strCrashOrder);
        onClickToToggleCrashDivVisibilityById(buttonToggleCrashVisibility, strCrashOrder, "anchorLink_" + strCrashOrder);
    }
}