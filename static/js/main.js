$(document).ready(function () {

    
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });



    // Predict
    $('#btn-predict').click(function () {


    //    if(! $('div.checkbox-group.required :checkbox:checked').length > 0){
    //        alert('Please check atleast one box');
    //    }


    //    else {

            console.log($('#upload-file')[0])
            var form_data = new FormData($('#upload-file')[0]);

            // Show loading animation
            $(this).hide();
            $('.loader').show();

            // Make prediction by calling api /predict
            
            $.ajax({
                type: 'POST',
                url: '/predict',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: true,
                success: function (data) {
                    // Get and display the result
                    $('.loader').hide();
                    $('#prediction').fadeIn(600);
                    $('#prediction').text(' Prediction: ' + data);                    
                    console.log('Success!');
                },
            });
        // }
    });
    

});
