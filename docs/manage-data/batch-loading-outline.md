# Batch Loading Outline

This is an outline of the batch loading process to aid in future work on the code such as potential debugging and enhancement, and to help understand the process as following the code is a little maze-like bouncing between a handful of files.

- [load_batch Management Command](#load_batch-management-command)
- [BatchLoader.load_batch](#batchloaderload_batch)
- [Process Batch XML](#process-batch-xml)
  - [Create Title Records](#create-title-records)
    - [Read MARC XML](#read-marc-xml)
  - [Load Pages](#load-pages)
    - [Process Page OCR](#process-page-ocr)
    - [Index Page in Solr](#index-page-in-solr)
- [Repeat and Complete](#repeat-and-complete)
  - [Load Error](#load-error)

## load_batch Management Command

The process begins with the `manage.py load_batch (batch_path)` management command. These management commands by default call the `handle` function within the corresponding file in `(app)/management/commands/` where `core` is the main app for the Open ONI Django project: https://github.com/open-oni/open-oni/blob/v1.0.6/core/management/commands/load_batch.py#L37

This function performs a couple sanity checks and then creates an instance of the `BatchLoader` class, passing in optional command line arguments for whether we will process OCR and generate word coordinates files. Creating an instance of a class calls the class's `__init__` function. https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L57.

Note how `self.____` class variables are set. These are accessible afterwards in all other class functions. For the `BatchLoader` class, two settings are stored in such class variables for reference later: `self.PROCESS_OCR` and `self.PROCESS_COORDINATES`. Execution returns to the `handle` function which then calls the `BatchLoader` instance's `load_batch` method with the required `batch_path` command line argument: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L97

## BatchLoader.load_batch

This function begins by creating another class variable for use throughout other `BatchLoader` class functions: `self.pages_processed`. Watch for this kind of code at the beginning of other class functions called throughout the process.

Next we perform checks on whether a directory exists with the `batch_path` from the initial command line argument. We create a symlink to the provided path if`batch_path` itself is not a symlink and is not a path descending from a `BATCH_STORAGE` path which is itself a symlink.

Once paths are sorted, we check whether the batch has already been loaded by checking the database. If it exists, we return the database `Batch` model record: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L131

If not, we log that a new batch is being created in both the log text and in the database as a new `LoadBatchEvent` model record.

Next a `Batch` record is created and stored in the `batch` variable. The `_get_batch` and `_create_batch` functions check if the batch is already loaded and verify the awardee code in the batch name fits an existing `Awardee` record before saving the record in the database: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L147

The line following calls `_sanity_check_batch` which checks the path to the validated batch file (`batch_1.xml`by default, among a list of other aliases) and saves it in the `batch` object: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L147

## Process Batch XML

The batch XML is read into the `doc` variable: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L154

`Reel` records are verified and created: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L156

Each issue in the XML is loaded based on the METS path in the batch XML: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L167

For each METS path, we call `_load_issue` to read the issue's METS / MODS XML and create an `Issue` record. This retrieves information from the XML via xpaths: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L227

Before saving the `Issue` record, we grab the LCCN from the XML. If the `Title` record associated with the LCCN has been created, simply retrieve it. If not, we must construct the `Title` record. Now is when the code begins to get a little maze-like: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L260

### Create Title Records

The source of information for each `Title` record is a MARC record URL controlled by `settings.MARC_RETRIEVAL_URLFORMAT`. This defaults to URLs to the Library of Congress, but may be configured to load local records not available from the Library of Congress in case their systems are down or have not been updated with title information. We use this URL as a parameter in calling the `load_titles` management command. This begins with the `__init__` function that defines some processing tracking variables, then the `handle` function is called which checks whether the MARC source is a local path or a web URL and call the target XML file with `xml_file_handler`: https://github.com/open-oni/open-oni/blob/v1.0.6/core/management/commands/load_titles.py#L91

This calls code in another file with the MARC XML resource as its argument `title_loader.load(marc_xml)`. The `load` function first initializes a `TitleLoader` instance. The `TitleLoader` class has an `__init__` which sets `self.` variables for processing tracking as well. Then the class's `load_file` function is called, again with the MARC XML as is argument: https://github.com/open-oni/open-oni/blob/v1.0.6/core/title_loader.py#L27

Here a callback function `load_record` is defined and then passed to the `map_xml` function imported from the [pymarc library](https://pypi.org/project/pymarc/). The pymarc library is using Python's built-in `xml.sax` library to parse the MARC records from XML: https://gitlab.com/pymarc/pymarc/-/blob/v4.0.0/pymarc/marcxml.py#L114

The callback function then calls the `TitleLoader` class's  `delete_bib` or `load_bib` function depending on each MARC record's contents. Generally we will be using `load_bib` to retrieve the LCCN title's information and create or update the `Title` record: https://github.com/open-oni/open-oni/blob/v1.0.6/core/title_loader.py#L62

#### Read MARC XML

In case we are updating a title's information, all `Title` record attributes and database foreign key associations are cleared first. Then we begin retrieving the information from MARC data. If one is looking to see which MARC fields are used and how, this is where to look. First, the `Title` record information is retrieved and saved to create/update the record. Then we call a handful of helper functions to create associated database records like `Language` and `Place` and save to connect them with the `Title` record: https://github.com/open-oni/open-oni/blob/v1.0.6/core/title_loader.py#L128

The MARC XML is then saved in the database as a `MARC` record.

Some titles are then deleted, depending on their MARC data and title URL: https://github.com/open-oni/open-oni/blob/v1.0.6/core/title_loader.py#L170

Execution returns to the `load_titles` management command and it calls code to index the titles in Solr: https://github.com/open-oni/open-oni/blob/v1.0.6/core/management/commands/load_titles.py#L51

Then execution returns to `_load_issue` and the new `Title` record and `Batch` record are associated with the `Issue` record and finally saved: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L266

Issue notes are are created as `IssueNote` records, and then we get to the last big part of the process where we load each page of an issue: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L286

### Load Pages

A `Page` record is created and metadata is pulled from the issue's XML and the batch's `Reel` record. The page record is associated with the title, the database record is saved, and `PageNote` records are added: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L293

The code reads the issue's XML for files associated with the page such as images, PDFs, and OCR files. Page image dimensions are stored in the database record, whether retrieved directly from the XML or calculated with the Python PIL library: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L378

#### Process Page OCR

If the page has an OCR file and `self.PROCESS_OCR` was set to true, we now process the page's OCR: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L414

The code constructs the full file path and then calls the function `ocr_extractor` whose code is in another file including its definition and the class `OCRHandler`: https://github.com/open-oni/open-oni/blob/v1.0.6/core/ocr_extractor.py#L67

We first create an instance of the `OCRHandler` class as `handler`. There are a few class attributes set in the `__init__` function and the `startElement` and `endElement` functions define how the XML will be parsed and stored within the class variables when the parser's `parse` function is called. Then we create a parser from the Python's built-in `xml.sax` library and assign `handler` to it before calling `parse`: https://github.com/open-oni/open-oni/blob/v1.0.6/core/ocr_extractor.py#L76

From the XML, this processes the `<Page>` element to store the page's width and height. Each opening `<TextBlock>` element designates the language of text elements within. These will be `<TextLine>` elements and `<String>` elements within those.

Each `<String>` element has its raw contents added to `_line` and tokenizes individual words scrubbed of special characters as keys for a dictionary `_coords` to work with how Solr indexes words for highlighting search results: 

https://github.com/open-oni/open-oni/blob/v1.0.6/core/ocr_extractor.py#L27

Each occurance of a word creates or appends its coordinates to a list at that word key in the `_coords` dictionary. As each `<TextLine>` element is closed, it joins all of the raw text in `_line` and creates or appends it to the page's dictionary of text languages based on the language set by the containing `<TextBlock>`. Once the `<Page>` element is closed, the lines for each language are joined with line breaks into a complete text for the page in each language. Then the `ocr_extractor` code completes by returning the dictionary of languages and their complete texts and a dictionary of the page width, height, and word coordinates dictionary back to the `process_ocr` function.

If `self.PROCESS_COORDINATES` is true, we write the word coordinates to a gzip compressed JSON file for the page: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L444

Next the OCR information is stored in the database. An `OCR` record is created, associated with the `Page` record, and saved. Then, for each language in the `lang_text` dictionary returned from `ocr_extractor` a `LanguageText` record is created with the text in the dictionary and associated with the `OCR` record.

#### Index Page in Solr

Next, the page's contents are indexed in Solr: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L440

We have to examine the `Page` model code to understand what comprises the fields indexed: https://github.com/open-oni/open-oni/blob/v1.0.6/core/models.py#L799

The date value is set, then information from the associated `Title` record is retrieved, with three fields `essay`, `url`, and `holding_type` deleted: https://github.com/open-oni/open-oni/blob/v1.0.6/core/models.py#L279

Additional fields are retrieved through the associated `Issue` and `Batch` records: https://github.com/open-oni/open-oni/blob/v1.0.6/core/models.py#L809

The associated `OCR` record and its associated `LanguageText` records are retrieved. We check whether the language code is in the list of languages to be used by one's Solr in `settings.SOLR_LANGUAGES` (or default to `eng` for English) and place the language's OCR text into a field with the language code prefixed with `ocr_`. The document is completed and added to Solr. We mark the `Page` record as indexed and save the change.

## Repeat and Complete

At this point we've completed the code in `_load_page`  and return to `_load_issue` and repeat for each of the issue's pages. Then we return to `_load_batch` and repeat for all of the batch's issues. After this we commit all changes to Solr's index and create another `LoadBatchEvent` to store how many pages were loaded into the site and print the same message to the log text.

### Load Error

If an error occurs during the batch load a message is printed to the text log and a `LoadBatchEvent` record is written to the database with the same message. After this, the code tries to automatically purge what was partially loaded from the batch: https://github.com/open-oni/open-oni/blob/v1.0.6/core/batch_loader.py#L193

This creates another `LoadBatchEvent` to record the attempt to purge the batch. The removal happens mostly in the reverse order of how things were added. Word coordinates files for pages are removed, then `Page` records, then `Issue` records, then the `Batch` record. After this, the documents in the Solr index with the batch's name are deleted. Any symlinks created for the batch are also removed. Lastly another `LoadBatchEvent` record is created to log whether the purge was successful or not.


