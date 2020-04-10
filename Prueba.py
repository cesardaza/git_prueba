import  scrapy
from  ..items import ResearchItem



class documentosSpider(scrapy.Spider):
    name = 'documentos'

    allowed_domain = ['https://www.researchgate.net']

    # Url de donde se va a sacar la informacion.
    #start_urls = ['https://www.researchgate.net/profile/Carlos_Cobos2']

    def __init__(self, url=None, *args, **kwargs):
         super(documentosSpider, self).__init__(*args, **kwargs)
         self.start_urls = ['%s' % url]


    def parse(self, response):
        #for href in response.xpath("//a[@class='nova-c-button nova-c-button--align-center nova-c-button--radius-m nova-c-button--size-s nova-c-button--color-blue nova-c-button--theme-bare nova-c-button--width-auto nova-v-publication-item__action']/@href") :
        for href in response.xpath('//div[@class="nova-v-publication-item__stack-item"]/div[1]/a/@href'):
            yield response.follow(href, self.parse_documentos)

    def parse_documentos(self,response):
        rg_item = ResearchItem()
        rg_item['Titulo'] = response.xpath('//section[@class="publication-details__section"]/h1/text()').extract_first()
        rg_item['Tipo'] = response.xpath('//span[@class="publication-meta__type"]/text()').extract_first()
        rg_item['Fecha'] = response.xpath('//div[@class="publication-meta"]/div/span[last()]/text()').extract_first(default='')
        rg_item['Num_lecturas'] = response.xpath('//div[@class="publication-meta"]/div/text()[last()]').extract_first(default='')
        rg_item['Autores'] = response.xpath('//div[@class="nova-v-person-list-item__align-content"]/div/a/text()').extract()
        rg_item['Abstrac'] = response.xpath('//div[@class="nova-c-card nova-c-card--spacing-m nova-c-card--elevation-none"]/div[2]/div/text()').extract()
        rg_item['Url'] = response.url
        yield rg_item