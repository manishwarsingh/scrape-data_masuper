import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import utils
from selenium.webdriver.common.action_chains import ActionChains



def get_product_info(driver, productUrl):
	driver.get(productUrl)
	time.sleep(10)
	handle = "NA"
	title = "NA"
	descText = "NA"
	vendor = "NA"
	category = "NA"
	tags = "NA"
	published = "NA"
	optionOutput = "NA"
	variantSKU = "NA"
	variantGrams = "NA"
	variantInventoryTracker = "NA"
	variantInventoryPolicy = "deny"
	variantFulfillmentService = "NA"
	variantPrice = "NA"
	variantCompareAtPrice = "NA"
	variantRequiresShipping = "NA"
	variantTaxable = "NA"
	variantBarcode = "NA"
	images = "NA"
	imagePosition = "NA"
	imageAltText = "NA"
	giftCard = "NA"	
	seoTitle = "NA"
	seoDescription = "NA"	
	googleShoppingGoogleProductCategory	= "NA"
	googleShoppingGender = "NA"
	googleShoppingAgeGroup = "NA"	
	googleShoppingMPN = "NA"	
	googleShoppingAdWordsGrouping = "NA"	
	googleShoppingAdWordsLabels	 = "NA"
	googleShoppingCondition	= "NA"
	googleShoppingCustomProduct	= "NA"
	googleShoppingCustomLabel0	= "NA"
	googleShoppingCustomLabel1	= "NA"
	googleShoppingCustomLabel2 = "NA"
	googleShoppingCustomLabel3 = "NA"	
	googleShoppingCustomLabel4 = "NA"
	variantImage = "NA"	
	variantWeightUnit = "NA"	
	variantTaxCode = "NA"	
	costPerItem	= "NA"
	status = "draft"

	try:
		title = driver.find_element(By.CSS_SELECTOR, "h1.h2.title-primary").text
	except Exception as e:
		print(e)
	try:
		costPerItem = driver.find_element(By.CSS_SELECTOR, "span#so-price").text
	except Exception as e:
		print(e)
	try:
		productImgs = driver.find_elements(By.CSS_SELECTOR, ".grid-item.medium-down--one-quarter img")
		productImages = [image.get_attribute('src') for image in productImgs]
		if len(productImages) > 0:
			images = {"image_"+str(i+1): k for i, k in enumerate(productImages)}
	except Exception as e:
		print(e)

	try:
		description = driver.find_element(By.XPATH, "//*[contains(text(), 'Description')]")
		if description:
			time.sleep(5)
			try:
				elem = driver.find_element(By.CSS_SELECTOR, "ul.tabs li:nth-child(1) a")
				actions = ActionChains(driver)
				actions.move_to_element(elem).click()
				actions.perform()
			except Exception as e:
				print(e)
			descText = driver.find_element(By.CSS_SELECTOR, ".grid-item.product-description.rte").text
		else:
			descText = "NA"
	except Exception as e:
		raise e

	try:
		category = driver.find_element(By.CSS_SELECTOR, "span.breadcrumb--truncate").text
	except Exception as e:
		print(e)

	try:
		optionsHead = driver.find_elements(By.CSS_SELECTOR, "form#addToCartForm .swatch.clearfix .header")
		optionsHead = [option.text for option in optionsHead]
		quantityHeader = driver.find_element(By.CSS_SELECTOR, "form#addToCartForm div#special-offer-v1 label.so-header").text
		optionsHead.append(quantityHeader)
		optionsVal = driver.find_elements(By.CSS_SELECTOR, "form#addToCartForm .swatch.clearfix .swatch-inner")
		optionsVal = [option.text for option in optionsVal]
		optionsVal = [x.replace('\n', ',') for x in optionsVal]
		quantityval = driver.find_elements(By.CSS_SELECTOR, "form#addToCartForm .so-options.so-design2 .so-selector")
		quantityvalue = [quantity.text for quantity in quantityval]
		quantityvalue = ', '.join(quantityvalue)
		optionsVal.append(quantityvalue)
		optionHead = {"Option "+str(i+1)+" Name": k for i, k in enumerate(optionsHead)}
		optionval = {"Option "+str(i+1)+" Value": k for i, k in enumerate(optionsVal)}
		optionHead.update(optionval)
		optionOutput = dict(sorted(optionHead.items()))
	except Exception as e:
		print(e)

	time.sleep(5)

	driver.switch_to.frame("looxReviewsFrame")
	# collect data for all reviews
	customerFeedback = []
	try:
		rev = driver.find_element(By.CSS_SELECTOR, "#grid")
		reviews = driver.find_elements(By.CSS_SELECTOR, ".grid-item.clearfix")
		for review in reviews:
			try:
				imageUrl = review.find_element(By.CSS_SELECTOR, ".item-img.box img").get_attribute("src")
			except Exception as e:
				imageUrl = "NA"
			try:
				customerId = review.find_element(By.CSS_SELECTOR, ".block.title").text
			except Exception as e:
				customerId = "NA"
			try:
				feedback = review.find_element(By.CSS_SELECTOR, ".pre-wrap.main-text.action").text
			except Exception as e:
				feedback = "NA"

			print(imageUrl, "imageurl")
			print(customerId, "customerId")
			print(feedback, "text")

			customerFeedback.append({
				"product_img_link":imageUrl,
				"feedback": feedback,
				"customer_id": customerId
				})

	except Exception as e:
		print("No reviews", e)

	feedback = {"customer_feedback": customerFeedback}

	product = {
		"Handle" : handle,
		"Title" : title,
		"Body" : descText,
		"Vendor" : vendor,
		"Type" : category,
		"Tags" : tags,
		"Published" : published
		}

	Variants = {
		"Variant SKU" : variantSKU,
		"Variant Grams" : variantGrams,
		"Variant Inventory Tracker" : variantInventoryTracker,
		"Variant Inventory Policy" : variantInventoryPolicy,
		"Variant  Fulfillment Service" : variantFulfillmentService,
		"Variant Price" : variantPrice,
		"Variant Compare At Price" : variantCompareAtPrice,
		"Variant Requires Shipping" : variantRequiresShipping,
		"Variant Taxable" : variantTaxable,
		"Variant Barcode" : variantBarcode
	}
		
	Others = {
		"Image Position" : imagePosition,
		"Image Alt Text" : imageAltText,
		"Gift Card" : giftCard,
		"SEO Title" : seoTitle,
		"SEO Description" : seoDescription,	
		"Google Shopping/Google Product Category": googleShoppingGoogleProductCategory,
		"Google Shopping/Gender" : googleShoppingGender,
		"Google Shopping /Age Group" : googleShoppingAgeGroup,
		"Google Shopping /MPN" : googleShoppingMPN,
		"Google Shopping /AdWords Grouping" : googleShoppingAdWordsGrouping,
		"Google Shopping /AdWords Labels": googleShoppingAdWordsLabels,
		"Google Shopping /Condition": googleShoppingCondition,
		"Google Shopping /CustomProduct" : googleShoppingCustomProduct,
		"Google Shopping/Custom Label 0" : googleShoppingCustomLabel0,
		"Google Shopping/Custom Label 1" : googleShoppingCustomLabel1,
		"Google Shopping/Custom Label 2" : googleShoppingCustomLabel2,
		"Google Shopping/Custom Label 3" : googleShoppingCustomLabel3,
		"Google Shopping/Custom Label 4" : googleShoppingCustomLabel4,
		"Variant Image" : variantImage,
		"Variant Weight Unit" : variantWeightUnit,	
		"Variant Tax Code" : variantTaxCode,
		"Cost Per Item"	: costPerItem,
		"Status" : status
	}
	#This is the contant you have to scrapr here using this script. 
	products.append(product | optionOutput | Variants| Others |  images | feedback)

#This function gives you all the products url from all the pages.
def get_product_type_info(driver, url):
	driver.get(url)
	productUrls = [typesUrl.get_attribute("href") for typesUrl in driver.find_elements(By.CSS_SELECTOR, ".product-grid-image--centered.simulate-link a")]
	if productUrls:
		for productUrl in productUrls: 
			try:
				get_product_info(driver, productUrl)
				print("product added")
			except Exception as e:
				print("Error on getting product type info", e)

try:
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-extensions")
	options.add_argument("--proxy-server='direct://'")
	options.add_argument("--proxy-bypass-list=*")
	options.add_argument("--start-maximized")
	#options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-sandbox')
	options.add_argument('--ignore-certificate-errors')
	options.add_experimental_option('extensionLoadTimeout', 60000)
	options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36");
	driver = webdriver.Chrome(executable_path= './chromedriver_windows/chromedriver', options=options)
	#Paste beloew the site url, you want to scrape.
	driver.get("https://***/***")
	
	categories = [categoryType.text for categoryType in driver.find_elements(By.CSS_SELECTOR, "h2.section-header--left.h1")]
	typesLinks = [typesUrl.get_attribute("href") for typesUrl in driver.find_elements(By.CSS_SELECTOR, ".section-header--right a")]
	categoryList = [(categories[i], typesLinks[i]) for i in range(0, len(categories))]
	if categoryList:
		for category in categoryList:
			productType, url = category
			print(productType, url)
			time.sleep(1)
			products = []
			try:
				get_product_type_info(driver, url)
				csvName = f"{productType}"+"_product"
				print("Creating Product CSV__product")
				utils.create_csv(products, csvName, productType)
				print("product type added")
			except Exception as e:
				 print("Error on getting product type info", e)	
except Exception as e:
	raise


