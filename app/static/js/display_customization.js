function applyGlobalStyles(baseSelector) {
    const jQueryBase = $(baseSelector);
    if (jQueryBase.length <= 0) {
        return;
    }

    // tables and non-table code blocks scroll horizontally on overflow
    jQueryBase.find("table").wrap(HORIZ_SCOLL_DIV_HTML);
    jQueryBase.find("pre").each(function() {
        if ($(this).parents("table").length === 0) {
            $(this).wrap(HORIZ_SCOLL_DIV_HTML);
        }
    });

    // inline CSS used by Markdown tables converted to class for CSP
    jQueryBase.find("[style='text-align: center;']").removeAttr("style").addClass("text-center");
    jQueryBase.find("[style='text-align: right;']").removeAttr("style").addClass("text-end");

    // no extra space between lists and their "heading" text
    jQueryBase.find("ol, ul").prev("p").addClass("mb-0");

    // footnote tweaks
    const jQueryFootnotes = jQueryBase.find(".footnote").first();
    if (jQueryFootnotes.length > 0) {
        jQueryFootnotes.attr("id", "footnotes");
        jQueryFootnotes.wrap("<details id=\"footnotes__details\" class=\"footnotes__details\"></details>")
        jQueryFootnotes.before("<summary class=\"footnotes__details-summary\">Footnotes</summary>");

        jQueryFootnotes.find("p").addClass("mb-0");
        const jQueryFootnotesList = jQueryFootnotes.children("ol").first();
        jQueryFootnotesList.addClass("mb-0");
        jQueryFootnotesList.children("li").addClass("mb-1");
    }

    // footnotes collapsible opens if footnote link clicked on and the collapsible is closed
    jQueryBase.find(".footnote-ref").on("click", function(e) {
        const jQueryFootnotesDetails = jQueryBase.find("#footnotes__details");
        if (!jQueryFootnotesDetails.is("[open]")) {
            jQueryFootnotesDetails.attr("open", "");
        }
    });
    
    applyCustomMarkdown(baseSelector); // Markdown tweaks round 3
    syntaxHighlightNonTable(baseSelector);
}

function applyCustomMarkdown(baseSelector) {
    const jQueryBase = $(baseSelector);
    if (jQueryBase.length <= 0) {
        return;
    }

    // custom table horizontal and vertical align syntax
    jQueryBase.find("[data-align-center]").parents("th, td").addClass("text-center");
    jQueryBase.find("[data-align-right]").parents("th, td").addClass("text-end");
    jQueryBase.find("[data-align-top]").parents("th, td").addClass("align-top");
    jQueryBase.find("[data-align-bottom]").parents("th, td").addClass("align-bottom");

    // custom table column width syntax
    jQueryBase.find("[data-col-width]").parents("th, td").attr("width", $(this).attr("data-col-width"));

    // no extra `<p>` tags in custom figures/captions
    jQueryBase.find(".md-captioned-figure").find("p").children("img").unwrap();
}

function genFootnoteTooltips(baseSelector) {
    const jQueryBase = $(baseSelector);
    if (jQueryBase.length <= 0) {
        return;
    }
    const REMOVE_BACKREF_RE = /<a class=["&quot;]+?footnote-backref[\S\s]*?<\/a>/;
    const MATCH_MATHJAX_RE = /<mjx-container[\S\s]*?<\/mjx-container>/g;

    jQueryBase.find(".footnote-ref").each(function() {
        $(this).attr("data-bs-toggle", "tooltip").attr("data-bs-html", "true");
        const nodeFootnote = document.getElementById($(this).attr("href").replace("#", ""));
        let tooltipContents = $(nodeFootnote).find("p").first().html().replace(REMOVE_BACKREF_RE, "");

        // replace serialized MathML HTML with its corresponding original LaTeX
        // to render with MathJax.typeset() on mouseover
        const mathItems = MathJax.startup.document.getMathItemsWithin(nodeFootnote);
        const matches = tooltipContents.match(MATCH_MATHJAX_RE);
        if (matches != null) {
            for (let i = 0; i < matches.length; i++) {
                let match = matches[i];
                tooltipContents = tooltipContents.replace(match, `\\(${mathItems[i].math}\\)`);
            }
        }

        $(this).attr("data-bs-title", tooltipContents);
    });

    refreshTooltips(baseSelector);
}

function syntaxHighlightNonTable(baseSelector) {
    $(baseSelector).find("pre code").each(function() {
        if ($(this).parents("table").length === 0) {
            hljs.highlightElement($(this).get(0));
            $(this).addClass("code-block--outside");
        }
    });
}

function reloadBackgroundImg() {
    if (urlBackgroundImgOverride !== "") {
        $("#background-img").css("background-image", `url(${urlBackgroundImgOverride})`);
    } else {
        $("#background-img").css("background-image", `url(${URL_BACKGROUND_IMG_DEFAULT})`);
    }
}

applyGlobalStyles("body");
reloadBackgroundImg();

$(document).ready(function() {
    // must wait until `$(document).ready()` to make sure MathJax has been loaded
    genFootnoteTooltips("body");
});
