// This is the jquery, we are not js programmers so
// this code might not look good

function updateBitrate() {
    $.ajax({
        url: "/get_bitrate",  // Update this URL with the endpoint of your Flask backend
        method: "GET",
        dataType: "json",
        success: function(data) {   
            // Update the bitrate in the HTML element
            $("#bitrate1").html(data.bitrate1 + " MB/s");
            $("#bitrate2").html(data.bitrate2 + " MB/s");
            $("#bitrate3").html(data.bitrate3 + " MB/s");
            $("#bitrate4").html(data.bitrate4 + " MB/s");
            $("#bitrate5").html(data.bitrate5 + " MB/s");
            sessionStorage.setItem('bitrate1', data.bitrate1 + " MB/s" );
            sessionStorage.setItem('bitrate2', data.bitrate2  + " MB/s");
            sessionStorage.setItem('bitrate3', data.bitrate3 + " MB/s" );
            sessionStorage.setItem('bitrate4', data.bitrate4 + " MB/s" );
            sessionStorage.setItem('bitrate5', data.bitrate5 + " MB/s" );
            console.log(bitrate1,bitrate2,bitrate3,bitrate4,bitrate5)
        },
        error: function(xhr, status, error) {
            console.error("Error fetching bitrate: " + error);
        }
      
        });
}

