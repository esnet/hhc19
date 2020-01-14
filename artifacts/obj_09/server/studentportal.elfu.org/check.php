<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="icon" href="favicon.ico" type="image/ico" >

    <!-- Google fonts CSS -->
    <link href="https://fonts.googleapis.com/css?family=Abril+Fatface|Roboto:300,400,500" rel="stylesheet">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">

    <!-- Fontawesome CSS -->
    <link href="/css/fa/css/all.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="css/style.css">

    <title>Merry Christmas</title>
</head>

<body class="login-page">
    <header class="header">
      <!-- Fixed navbar -->
      <!-- Fixed navbar -->
<nav class="navbar navbar-expand-lg  fixed-top ">
    <button class="btn btn-dark navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="fa fa-bars text-white"></span>
    </button>
    <a class="navbar-brand" href="/"><i class="fa fa-snowflake"></i><span class="text-sm-hide ml-2">Elf University</span></a>

    <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
                <a class="nav-link " href="index.php">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="students.php">Student Body</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="apply.php">Apply Now</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="check.php">Check Application Status</a>
            </li>
        </ul>
    </div>
</nav>
    </header>

    <!-- Begin page content -->
    <main role="main" class="main-container ">
        <div class="container-fluid ">
            <div class="row vhf-100">
                <div class="col-12 col-lg-6 no-float">
                    <div class="row h-100 align-items-center py-4">
                        <div class="col-12 col-sm-8 col-lg-6 mx-auto text-center">
                          <div class="row mt-5">
                          </div>
                            <form id="check" action="/application-check.php" method="get" class="form-signin mb-5" onSubmit="submitApplication()">
                                <br/>
                                <h1 class="display-4 mb-5 font-weight-normal">Check Application Status</h1>
                                <div class="form-group">
                                    <label for="inputEmail" class="sr-only">Elf Mail Address</label>
                                    <input name="elfmail" type="email" id="inputEmail" class="form-control form-control-lg" placeholder="Email address" required="" autofocus="">
                                </div>
                                <input type="hidden" id="token" name="token" value=""/>
                                <div class="row">
                                    <div class="col-12 text-center">
                                        <input type='submit' class="btn btn-danger btn-lg mt-4 px-5" value="Check Status" />
                                    </div>
                                </div>

                            </form>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-lg-6 no-float" style='height: 1000px'>
                    <div class="background-img dark-img" style="background-image: url(img/topbanner.jpg);"></div>
                    <div class="row h-100 align-items-center py-4">
                        <div class="col-12 col-sm-8 mx-auto text-center text-white">
                            <h1 class="display-4 mb-4">How's your application doing?</h1>
                            <p class="lead">Where happiness and cheer are all you'll hear!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>

    <!--  Custom js -->
    <script>

    function submitApplication() {
      console.log("Submitting");
      elfSign();
      document.getElementById("check").submit();
    }
    function elfSign() {
      var s = document.getElementById("token");

      const Http = new XMLHttpRequest();
      const url='/validator.php';
      Http.open("GET", url, false);
      Http.send(null);

      if (Http.status === 200) {
        console.log(Http.responseText);
        s.value = Http.responseText;
      }

    }

    </script>





    <script src="js/main.js"></script>
</body>

</html>
