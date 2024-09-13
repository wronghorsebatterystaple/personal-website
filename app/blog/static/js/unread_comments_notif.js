const jQueryIconBell = $("#icon--btn-comments-unread-notif");

// when logging in via modal on a `blog.` page/opening a `blog.` page as admin, check for notifications
onModalLogin = addToFunction(onModalLogin, function() {
    updateUnreadCommentsNotifs();
});
$(document).ready(function() {
    if (isUserAuthenticated) {
        updateUnreadCommentsNotifs();
    }
});

async function updateUnreadCommentsNotifs() {
    let notifCount = await updateUnreadCommentsDropdown();
    if (notifCount > 0) {
        setBellWithNotif();
    } else {
        setBellWithoutNotif();
    }
}

function setBellWithNotif() {
    jQueryIconBell.removeClass("bi-bell");
    jQueryIconBell.addClass("bi-bell-fill");
}

function setBellWithoutNotif() {
    jQueryIconBell.removeClass("bi-bell-fill");
    jQueryIconBell.addClass("bi-bell");
}

async function updateUnreadCommentsDropdown() {
    const jQueryDropdownCommentsUnread = $("#dropdown--comments-unread");

    // get posts with unread comments
    jQueryDropdownCommentsUnread.html("<span class=\"dropdown-item\">Loading…</span>");
    const respJson = await fetchWrapper(URL_GET_POSTS_WITH_UNREAD_COMMENTS, {method: "POST"});

    if (respJson.errorStatus) {
        jQueryDropdownCommentsUnread.html("<span class=\"dropdown-item\">Unable to load posts :/</span>");
        return -1;
    }

    if (respJson.relogin) {
        jQueryDropdownCommentsUnread.html("<span class=\"dropdown-item\">Not so fast :]</span>");
        return -1;
    }

    let postCount = Object.keys(respJson).length;
    if (postCount === 0) {
        jQueryDropdownCommentsUnread.html("<span class=\"dropdown-item\">There's nothing here :]</span>");
        return postCount;
    }

    let html = "";
    for (const [postTitle, v] of Object.entries(respJson)) {
        html += `<a class="dropdown-item" href="${v.url}"><span class="custom-pink">(${v.unread_count})</span> ${postTitle}</a>`;
    }
    jQueryDropdownCommentsUnread.html(html);

    return postCount;
}

/**
 * Aligns dropdown to the left of its button (since it's on the right of the screen; we don't want overflow).
 */
const styleSheetDropdownAlign = new CSSStyleSheet();
document.adoptedStyleSheets.push(styleSheetDropdownAlign);
function alignDropdownLeftwards(records) {
    const nodeDropdown = records[0].target;
    let offset = nodeDropdown.offsetWidth - document.querySelector("#btn--unread-comments-notif").offsetWidth;
    styleSheetDropdownAlign.replaceSync(`:root { --dropdown-comments-unread-left: -${offset}px; }`);
}

$(document).ready(function() {
    // observe for changes in innerHTML to re-align the dropdown leftwards
    const mutationObserver = new MutationObserver(alignDropdownLeftwards);
    mutationObserver.observe(document.querySelector("#dropdown--comments-unread"), {
        childList: true
    });

    // refresh notifications on click
    $("#btn--unread-comments-notif").on("click", function() {
        updateUnreadCommentsNotifs();
    });
});
