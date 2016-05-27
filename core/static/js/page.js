(function($) {
    var page_url;
    var coordinates_url;
    var navigation_url;
    var width;
    var height;
    var static_url;

    function disablePrint(viewer) {
        $("#clip").attr('href', "");
        $("#clip").addClass("disabled");
    }

    function resizePrint(event) {
        var viewer = event.eventSource;
        var image = viewer.source;
        var zoom = viewer.viewport.getZoom(); 
        var size = new OpenSeadragon.Rect(0, 0, image.dimensions.x, image.dimensions.y);
        var container = viewer.viewport.getContainerSize();
        var fit_source = fitWithinBoundingBox(size, container);
        var total_zoom = fit_source.x/image.dimensions.x;
        var container_zoom = fit_source.x/container.x;
        var level =  (zoom * total_zoom) / container_zoom;
        var box = getDisplayRegion(viewer, new OpenSeadragon.Point(parseInt(image.dimensions.x*level), parseInt(image.dimensions.y*level)));
        var scaledBox = new OpenSeadragon.Rect(parseInt(box.x/level), parseInt(box.y/level), parseInt(box.width/level), parseInt(box.height/level));
        var d = fitWithinBoundingBox(box, new OpenSeadragon.Point(681, 817));
        var dimension = page_url+'print/image_'+d.x+'x'+d.y+'_from_'+ scaledBox.x+','+scaledBox.y+'_to_'+scaledBox.getBottomRight().x+','+scaledBox.getBottomRight().y;
        $("#clip").attr('href', dimension);
        $("#clip").removeClass("disabled");
        $(".locshare-print-button").find('a:first').attr('href', dimension).click(function(event) {
            window.open($(this).attr('href'), "print");
        });
    };

    function fitWithinBoundingBox(d, max) {
        if (d.width/d.height > max.x/max.y) {
            return new OpenSeadragon.Point(max.x, parseInt(d.height * max.x/d.width));
        } else {
            return new OpenSeadragon.Point(parseInt(d.width * max.y/d.height),max.y);
        }
    }
    
    function getDisplayRegion(viewer, source) {
        //Determine portion of scaled image that is being displayed
        var box = new OpenSeadragon.Rect(0, 0, source.x, source.y);
        var container = viewer.viewport.getContainerSize();
        var bounds = viewer.viewport.getBounds();
        //If image is offset to the left
        if (bounds.x > 0){
            box.x = box.x - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).x;
        }
        //If full image doesn't fit
        if (box.x + source.x > container.x) {
            box.width = container.x - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).x;
            if (box.width > container.x) {
                box.width = container.x;
            }
        }
        //If image is offset up
        if (bounds.y > 0) {
            box.y = box.y - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).y;
        }
        //If full image doesn't fit
        if (box.y + source.y > container.y) {
            box.height = container.y - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).y;
            if (box.height > container.y) {
                box.height = container.y;
            }
        }
        return box;
    }

    function addOverlay(viewer, x1, y1, x2, y2) {
        var img = document.createElement("img");
        var placement = OpenSeadragon.OverlayPlacement.BOTTOM;
            
        var div = document.createElement("div");
        var rect = new OpenSeadragon.Rect(x1, y1, x2, y2);

        div.className = "overlay";
        viewer.drawer.addOverlay(div, rect);
    }

    function addOverlays(event) {
        var viewer = event.eventSource;
        var params = $.deparam.fragment();
        var words = params["words"] || "";
        var dimensions = viewer.source.dimensions;
        $.getJSON(coordinates_url, function(all_coordinates) {
            var scale = 1 / all_coordinates["width"];
            
            $.each(words.split(" "), function(index, word) {
                if (word!="") {
                    var boxes = [];

                    var coordinates = all_coordinates["coords"][word];
                    if(coordinates !== undefined){
                        $.each(coordinates, function(index, value) {
                            addOverlay(viewer,
                                       value[0]*scale,
                                       value[1]*scale,
                                       value[2]*scale,
                                       value[3]*scale);
                        });
                    }
                }
            });
        });
    }

    function initPage() {
        page_url = $('#page_data').data("page_url")
        coordinates_url = $('#page_data').data("coordinates_url")
        navigation_url = $('#page_data').data("navigation_url")
        width = $('#page_data').data("width")
        height = $('#page_data').data("height")
        static_url = $('#page_data').data("static_url")
        iiif_id = $('#page_data').data("iiif_id")

        var viewer = null;

        var viewer = OpenSeadragon({
            id: "viewer_container",
            toolbar: "item-ctrl",
            prefixUrl: static_url,
            autoHideControls: false,
            showNavigator: true,
            nextButton: "next",
            previousButton: "previous",
            timeout: 60000,
            tileSources: iiif_id
        });

        viewer.addHandler("open", addOverlays);
        viewer.addHandler("open", resizePrint);
        viewer.addHandler("animation-finish", resizePrint);
        viewer.addHandler("animation-start", disablePrint);

        $("#pageNum").change(function(event) { 
            page_url = $("#pageNum").val();
            window.location = page_url;
        });

    }
    $(initPage);
})(jQuery)
