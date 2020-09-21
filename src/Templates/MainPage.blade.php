<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OXDictionary</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
     <style>
       body,body>div{
           height:100vh;
       }
       body{
           background: linear-gradient(to right bottom,#f7f5fb 50%,#fff 50%)
       }
       form{
           max-width:600px;
           width:80%;
       }
     </style>
</head>
<body>
    <div class="mx-90 d-flex align-items-center justify-content-center">
         <form  method="post" class="card p-4">
            <div class="form-group">
                <h1 class="text-center"> Search</h1>
            </div>
            <div class="form-group d-flex">
                <input type="text" class="form-control" id="exampleInputPassword1" name="word" min="4" max="20" value="<?php echo $_POST['word'];?>">
                <button class="btn btn-danger">Submit</button>
            </div>
            <div class="pt-3">
               <?php
                 if (!empty($results) && isset($results)):
                ?>  
                 <h6 class="text-center">Definitions</h6>
                <?php  
                   foreach( $results as $item):
                        foreach ($item as $key => $value) :
                            if($key=="definitions"):
               ?>
                 <div class="alert alert-primary" role="alert">
                         <ul>
                             <?php
                              foreach ($value as $definition):
                             ?>
                             <li><?= $definition;?></li>
                             <?php
                              endforeach;
                             ?>
                         </ul>
                 </div>
               <?php    
                            endif;
                     endforeach;
                    endforeach;
                elseif (isset($error)):   
               ?>    
                <div class="alert alert-danger">
                  Your word doesn't exist
                </div>
               <?php 
               endif;
               ?>
            </div>
         </form>
    </div>
</body>
</html>