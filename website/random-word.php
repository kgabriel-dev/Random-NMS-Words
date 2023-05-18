<?php

    try {
        $language = $_GET['language'];
        randomWord($language);
    } catch(Exception $e) {
        http_response_code(400);
        print('Error: An error occurred. Please try again later.');
    }
    

    function getRandomLanguageFile() {
        $path = __DIR__ . "/languages/";
        $files = scandir($path);

        $language_files = array();
        foreach($files as $file) {
            if(str_ends_with($file, ".txt")) {
                array_push($language_files, $file);
            }
        }

        $randomFile = $language_files[array_rand($language_files)];
        return $randomFile;
    }

    function randomWord($language) {
        $language_file = NULL;

        if(!empty($language) && in_array($language, ['Gek', htmlspecialchars_decode('Vy&#39;keen'), 'Korvax'])) {
            $language_file = $language . ".txt";
        }
        else {
            $language_file = getRandomLanguageFile();
        }

        if(!file_exists(__DIR__ . "/languages/" . $language_file)) {
            http_response_code(400);
            print("Error: File not found");
            return;
        }

        $complete_file_path = __DIR__ . "/languages/" . $language_file;

        $fileObject = new \SplFileObject($complete_file_path);
        $fileObject->seek(0);
        $word_count = intval($fileObject->current());

        // Get random word
        $index = rand(0, $word_count);
        $fileObject->seek($index);
        
        $word = $fileObject->current();
        $word = str_replace("\n", "", $word);
        $word = str_replace("\r", "", $word);

        $language = basename($language_file, ".txt");

        http_response_code(200);
        print json_encode(array("word" => $word, "language" => $language));
    }
?>