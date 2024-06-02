from bs4 import BeautifulSoup


def extract_fragrance_brands(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    brand_divs = soup.find_all('div', class_='nmarca')

    brands = [div.get('data-nombre_marca') for div in brand_divs]

    return brands


# Example usage
html_content = """<div id="div_marcas_alf" style="clear: both; margin-top: 8px; background-color: #f9f9f9;" class="collapse_marcas">
                                                                                    <div class="letra_cabecera letra_cabecera_A">A</div>
                                                            <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Abercrombie &amp; fitch" data-nombre_marca_id="1516" data-logo="logos/logo__20171017153452.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Abercrombie &amp; fitch</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Acqua di parma" data-nombre_marca_id="200" data-logo="logos/yvuf1_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Acqua di parma</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Acqua di selva" data-nombre_marca_id="212" data-logo="logos/logo_212_20150525135855.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Acqua di selva</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Adidas" data-nombre_marca_id="2" data-logo="logos/logo_2_20150525101605.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Adidas</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Adolfo domínguez" data-nombre_marca_id="3" data-logo="logos/bFr0S_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Adolfo domínguez</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Afnan" data-nombre_marca_id="2617" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Afnan</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Agua de sevilla" data-nombre_marca_id="201" data-logo="logos/logo_201_20150525121526.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Agua de sevilla</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Aigner" data-nombre_marca_id="293" data-logo="logos/logo_293_20150525164913.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Aigner</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Alvarez gomez" data-nombre_marca_id="202" data-logo="logos/logo_202_20150525134347.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Alvarez gomez</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Alyssa ashley" data-nombre_marca_id="6" data-logo="logos/logo_6_20150525110416.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Alyssa ashley</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Amouage" data-nombre_marca_id="1173" data-logo="logos/logo_7015_20151020120913.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Amouage</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Angel schlesser" data-nombre_marca_id="7" data-logo="logos/oUmEB_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Angel schlesser</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Annayake" data-nombre_marca_id="4162" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Annayake</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Antonio banderas" data-nombre_marca_id="274" data-logo="logos/logo_274_20150525123435.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Antonio banderas</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Aramis" data-nombre_marca_id="8" data-logo="logos/logo_8_20150525110334.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Aramis</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Armaf" data-nombre_marca_id="1821" data-logo="logos/KQsV3_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Armaf</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Armand basi" data-nombre_marca_id="9" data-logo="logos/logo_9_20150525110323.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Armand basi</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca activo hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Armani" data-nombre_marca_id="10" data-logo="logos/LV9LS_2024-05-27.jpg">
                                <i class="fa fa-dot-circle-o" aria-hidden="true"></i> <span>Armani</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Atkinsons" data-nombre_marca_id="12" data-logo="logos/logo_12_20150525110227.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Atkinsons</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Axe" data-nombre_marca_id="13" data-logo="logos/WuhIw_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Axe</span>
                            </div>
                                                                                <div id="letra_A" class="nmarca letra_A div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Azzaro" data-nombre_marca_id="14" data-logo="logos/HQ597_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Azzaro</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_B">B</div>
                                                            <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Baldessarini" data-nombre_marca_id="203" data-logo="logos/logo_203_20150525134528.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Baldessarini</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Banani" data-nombre_marca_id="152" data-logo="logos/logo_152_20150525112222.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Banani</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Basi" data-nombre_marca_id="9" data-logo="logos/logo_9_20150525110323.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Basi</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Benetton" data-nombre_marca_id="227" data-logo="logos/logo_227_20150525125942.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Benetton</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Bentley" data-nombre_marca_id="228" data-logo="logos/logo_228_20150525155422.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Bentley</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Biagiotti" data-nombre_marca_id="78" data-logo="logos/logo_78_20150525095649.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Biagiotti</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Bien-etre" data-nombre_marca_id="275" data-logo="logos/logo_275_20150526085925.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Bien-etre</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Blood concept" data-nombre_marca_id="1272" data-logo="logos/logo__20160921170154.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Blood concept</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Boss" data-nombre_marca_id="61" data-logo="logos/yyPw7_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Boss</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Boucheron" data-nombre_marca_id="16" data-logo="logos/xb0CD_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Boucheron</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Brummel" data-nombre_marca_id="1051" data-logo="logos/logo_1051_20150611132006.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Brummel</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Bruno banani" data-nombre_marca_id="152" data-logo="logos/logo_152_20150525112222.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Bruno banani</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Bultaco" data-nombre_marca_id="2239" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Bultaco</span>
                            </div>
                                                                                <div id="letra_B" class="nmarca letra_B div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Bvlgari" data-nombre_marca_id="19" data-logo="logos/8y2VR_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Bvlgari</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_C">C</div>
                                                            <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Cacharel" data-nombre_marca_id="20" data-logo="logos/zkHXa_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Cacharel</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Calvin klein	" data-nombre_marca_id="21" data-logo="logos/BNrba_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Calvin klein	</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Carolina herrera" data-nombre_marca_id="22" data-logo="logos/rPqTv_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Carolina herrera</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Cartier" data-nombre_marca_id="24" data-logo="logos/swRzW_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Cartier</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Caudalie" data-nombre_marca_id="1279" data-logo="logos/logo_7130_20170203161304.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Caudalie</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Cavalli" data-nombre_marca_id="115" data-logo="logos/logo_115_20150525101916.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Cavalli</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Cerruti" data-nombre_marca_id="25" data-logo="logos/logo_25_20150525101029.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Cerruti</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Chanel" data-nombre_marca_id="26" data-logo="logos/go68w_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Chanel</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Christian dior" data-nombre_marca_id="30" data-logo="logos/8ZyHX_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Christian dior</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Clean" data-nombre_marca_id="1156" data-logo="logos/logo_6998_20151020122735.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Clean</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Clinique" data-nombre_marca_id="32" data-logo="logos/kBFXU_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Clinique</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Coach" data-nombre_marca_id="1515" data-logo="logos/logo__20170928113023.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Coach</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Coquette" data-nombre_marca_id="1661" data-logo="logos/logo_7545_20211117151341.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Coquette</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Coronel tapiocca" data-nombre_marca_id="1841" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Coronel tapiocca</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Couture" data-nombre_marca_id="176" data-logo="logos/PRAGB_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Couture</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Creed" data-nombre_marca_id="279" data-logo="logos/logo_279_20150525162848.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Creed</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Cristiano ronaldo" data-nombre_marca_id="1658" data-logo="logos/logo_7542_20211112171043.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Cristiano ronaldo</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Crossmen
" data-nombre_marca_id="1092" data-logo="logos/logo_1092_20150609085234.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Crossmen
</span>
                            </div>
                                                                                <div id="letra_C" class="nmarca letra_C div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Cuba" data-nombre_marca_id="280" data-logo="logos/logo_280_20150525162725.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Cuba</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_D">D</div>
                                                            <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="David beckham" data-nombre_marca_id="328" data-logo="logos/logo_328_20150611120102.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>David beckham</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Davidoff" data-nombre_marca_id="35" data-logo="logos/Dvoyr_2024-05-29.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Davidoff</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Diesel" data-nombre_marca_id="36" data-logo="logos/j6uei_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Diesel</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Dior" data-nombre_marca_id="30" data-logo="logos/8ZyHX_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Dior</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Dkny" data-nombre_marca_id="38" data-logo="logos/Dkva1_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Dkny</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Dolce &amp; gabbana" data-nombre_marca_id="1225" data-logo="logos/5WXfo_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Dolce &amp; gabbana</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Domínguez" data-nombre_marca_id="3" data-logo="logos/bFr0S_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Domínguez</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Don algodon" data-nombre_marca_id="1162" data-logo="logos/logo_7004_20151020124911.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Don algodon</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Dsquared2" data-nombre_marca_id="160" data-logo="logos/logo_160_20150525125834.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Dsquared2</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Duck" data-nombre_marca_id="81" data-logo="logos/logo_81_20150525095529.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Duck</span>
                            </div>
                                                                                <div id="letra_D" class="nmarca letra_D div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Dunhill" data-nombre_marca_id="41" data-logo="logos/logo_41_20150525100714.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Dunhill</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_E">E</div>
                                                            <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="El ganso" data-nombre_marca_id="1544" data-logo="logos/logo_7428_20190924123942.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>El ganso</span>
                            </div>
                                                                                <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Emanuel ungaro" data-nombre_marca_id="44" data-logo="logos/logo_44_20150525100627.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Emanuel ungaro</span>
                            </div>
                                                                                <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca activo hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Emporio armani" data-nombre_marca_id="10" data-logo="logos/LV9LS_2024-05-27.jpg">
                                <i class="fa fa-dot-circle-o" aria-hidden="true"></i> <span>Emporio armani</span>
                            </div>
                                                                                <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Escentric molecules" data-nombre_marca_id="272" data-logo="logos/logo_272_20150525172354.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Escentric molecules</span>
                            </div>
                                                                                <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Estée lauder" data-nombre_marca_id="48" data-logo="logos/NuRpu_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Estée lauder</span>
                            </div>
                                                                                <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Etro" data-nombre_marca_id="282" data-logo="logos/logo_282_20150610120755.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Etro</span>
                            </div>
                                                                                <div id="letra_E" class="nmarca letra_E div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Euroluxe" data-nombre_marca_id="1169" data-logo="logos/logo_7011_20151020125915.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Euroluxe</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_F">F</div>
                                                            <div id="letra_F" class="nmarca letra_F div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="F.c. barcelona" data-nombre_marca_id="2312" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>F.c. barcelona</span>
                            </div>
                                                                                <div id="letra_F" class="nmarca letra_F div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Faberge" data-nombre_marca_id="233" data-logo="logos/logo_233_20150525155955.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Faberge</span>
                            </div>
                                                                                <div id="letra_F" class="nmarca letra_F div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Façonnable" data-nombre_marca_id="234" data-logo="logos/logo_234_20150525163319.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Façonnable</span>
                            </div>
                                                                                <div id="letra_F" class="nmarca letra_F div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Ferrari" data-nombre_marca_id="49" data-logo="logos/logo_49_20150525100529.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Ferrari</span>
                            </div>
                                                                                <div id="letra_F" class="nmarca letra_F div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Franck olivier" data-nombre_marca_id="1190" data-logo="logos/logo_7032_20151020131110.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Franck olivier</span>
                            </div>
                                                                                <div id="letra_F" class="nmarca letra_F div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Frozen" data-nombre_marca_id="2026" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Frozen</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_G">G</div>
                                                            <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Gaultier" data-nombre_marca_id="64" data-logo="logos/4OAdf_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Gaultier</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Geoffrey beene" data-nombre_marca_id="284" data-logo="logos/logo_284_20150525124217.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Geoffrey beene</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca activo hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Giorgio armani" data-nombre_marca_id="10" data-logo="logos/LV9LS_2024-05-27.jpg">
                                <i class="fa fa-dot-circle-o" aria-hidden="true"></i> <span>Giorgio armani</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Giorgio beverly" data-nombre_marca_id="53" data-logo="logos/logo_45_20151020131634.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Giorgio beverly</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Givenchy" data-nombre_marca_id="54" data-logo="logos/BJ0g2_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Givenchy</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Guerlain" data-nombre_marca_id="56" data-logo="logos/8LfLT_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Guerlain</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Guess" data-nombre_marca_id="172" data-logo="logos/logo_172_20150525112506.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Guess</span>
                            </div>
                                                                                <div id="letra_G" class="nmarca letra_G div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Guy laroche" data-nombre_marca_id="57" data-logo="logos/logo_57_20150525100331.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Guy laroche</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_H">H</div>
                                                            <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Hackett london" data-nombre_marca_id="1808" data-logo="logos/logo_7692_20220826163007.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Hackett london</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Halloween" data-nombre_marca_id="1581" data-logo="logos/vUfRe_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Halloween</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Halston" data-nombre_marca_id="281" data-logo="logos/logo_281_20150525162419.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Halston</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Hannibal laguna" data-nombre_marca_id="1664" data-logo="logos/logo_7548_20211217085844.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Hannibal laguna</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Heno de pravia" data-nombre_marca_id="1613" data-logo="logos/logo_7497_20210416092901.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Heno de pravia</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Hermès" data-nombre_marca_id="60" data-logo="logos/rcd25_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Hermès</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Herrera" data-nombre_marca_id="22" data-logo="logos/rPqTv_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Herrera</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Hilfiger" data-nombre_marca_id="131" data-logo="logos/Lbkcq_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Hilfiger</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Hollister" data-nombre_marca_id="1532" data-logo="logos/logo_7416_20190220122257.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Hollister</span>
                            </div>
                                                                                <div id="letra_H" class="nmarca letra_H div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Hugo boss" data-nombre_marca_id="61" data-logo="logos/yyPw7_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Hugo boss</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_I">I</div>
                                                            <div id="letra_I" class="nmarca letra_I div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Iceberg" data-nombre_marca_id="237" data-logo="logos/logo_237_20150525161130.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Iceberg</span>
                            </div>
                                                                                <div id="letra_I" class="nmarca letra_I div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Instituto español" data-nombre_marca_id="1211" data-logo="logos/logo_7057_20151020135237.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Instituto español</span>
                            </div>
                                                                                <div id="letra_I" class="nmarca letra_I div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Issey miyake" data-nombre_marca_id="63" data-logo="logos/3dlas_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Issey miyake</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_J">J</div>
                                                            <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jacomo" data-nombre_marca_id="240" data-logo="logos/logo_240_20150525170313.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jacomo</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jacq's" data-nombre_marca_id="1220" data-logo="logos/logo_7071_20151020151308.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jacq's</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jacques bogart" data-nombre_marca_id="1057" data-logo="logos/logo_1057_20150611132125.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jacques bogart</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jaguar" data-nombre_marca_id="242" data-logo="logos/logo_242_20150525164156.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jaguar</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jean paul gaultier" data-nombre_marca_id="64" data-logo="logos/4OAdf_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jean paul gaultier</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jesús del pozo" data-nombre_marca_id="1581" data-logo="logos/vUfRe_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jesús del pozo</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jil sander" data-nombre_marca_id="246" data-logo="logos/logo_246_20150525172530.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jil sander</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jimmy choo" data-nombre_marca_id="217" data-logo="logos/logo_217_20150525150549.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jimmy choo</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Jo malone" data-nombre_marca_id="1209" data-logo="logos/logo__20150715152550.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Jo malone</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="John varvatos" data-nombre_marca_id="326" data-logo="logos/logo_326_20150611115621.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>John varvatos</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Joop!" data-nombre_marca_id="67" data-logo="logos/logo_67_20150525095933.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Joop!</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Juicy couture" data-nombre_marca_id="176" data-logo="logos/PRAGB_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Juicy couture</span>
                            </div>
                                                                                <div id="letra_J" class="nmarca letra_J div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Juliette has a gun" data-nombre_marca_id="1536" data-logo="logos/logo_7420_20190618154319.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Juliette has a gun</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_K">K</div>
                                                            <div id="letra_K" class="nmarca letra_K div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Karl lagerfeld" data-nombre_marca_id="219" data-logo="logos/logo_219_20150525153719.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Karl lagerfeld</span>
                            </div>
                                                                                <div id="letra_K" class="nmarca letra_K div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Kenzo" data-nombre_marca_id="70" data-logo="logos/Sw5m8_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Kenzo</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_L">L</div>
                                                            <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="L'occitane" data-nombre_marca_id="324" data-logo="logos/logo_324_20150611115402.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>L'occitane</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lacoste" data-nombre_marca_id="74" data-logo="logos/tKCwy_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lacoste</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lalique" data-nombre_marca_id="247" data-logo="logos/logo_247_20150526081549.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lalique</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lamborghini" data-nombre_marca_id="2526" data-logo="logos/logo_8410_20230214100034.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lamborghini</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lanvin" data-nombre_marca_id="77" data-logo="logos/logo_77_20150525095710.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lanvin</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Laroche" data-nombre_marca_id="57" data-logo="logos/logo_57_20150525100331.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Laroche</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lattafa" data-nombre_marca_id="4101" data-logo="logos/xsBDG_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lattafa</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lauder" data-nombre_marca_id="48" data-logo="logos/NuRpu_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lauder</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Laura biagiotti" data-nombre_marca_id="78" data-logo="logos/logo_78_20150525095649.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Laura biagiotti</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lauren" data-nombre_marca_id="111" data-logo="logos/9y9IS_2024-05-29.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lauren</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Legrain" data-nombre_marca_id="1193" data-logo="logos/logo_7035_20151022152106.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Legrain</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lempicka" data-nombre_marca_id="80" data-logo="logos/logo_80_20150525095621.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lempicka</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Loewe" data-nombre_marca_id="79" data-logo="logos/UBDTn_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Loewe</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Lolita lempicka" data-nombre_marca_id="80" data-logo="logos/logo_80_20150525095621.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Lolita lempicka</span>
                            </div>
                                                                                <div id="letra_L" class="nmarca letra_L div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Luxana" data-nombre_marca_id="1595" data-logo="logos/logo_7479_20210224122231.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Luxana</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_M">M</div>
                                                            <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Mancera paris" data-nombre_marca_id="1270" data-logo="logos/N6ILV_2024-05-23.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Mancera paris</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Mandarina duck" data-nombre_marca_id="81" data-logo="logos/logo_81_20150525095529.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Mandarina duck</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Marbert" data-nombre_marca_id="1032" data-logo="logos/logo_1032_20150611131201.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Marbert</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Mauboussin" data-nombre_marca_id="254" data-logo="logos/logo_254_20150525162909.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Mauboussin</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Mercedes-benz

" data-nombre_marca_id="221" data-logo="logos/logo_221_20150525154211.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Mercedes-benz

</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Ministry of oud" data-nombre_marca_id="4140" data-logo="logos/logo_10025_20230808093022.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Ministry of oud</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Missoni" data-nombre_marca_id="1537" data-logo="logos/logo_7421_20190620110540.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Missoni</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Miyake" data-nombre_marca_id="63" data-logo="logos/3dlas_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Miyake</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Monotheme" data-nombre_marca_id="365" data-logo="logos/logo_365_20150611135016.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Monotheme</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Montale" data-nombre_marca_id="1043" data-logo="logos/logo_1043_20150611165146.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Montale</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Montblanc" data-nombre_marca_id="88" data-logo="logos/iH1Pv_2024-05-29.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Montblanc</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Moschino" data-nombre_marca_id="89" data-logo="logos/vMNzR_2024-05-29.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Moschino</span>
                            </div>
                                                                                <div id="letra_M" class="nmarca letra_M div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Mugler" data-nombre_marca_id="129" data-logo="logos/FHNuE_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Mugler</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_N">N</div>
                                                            <div id="letra_N" class="nmarca letra_N div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Narciso rodríguez" data-nombre_marca_id="90" data-logo="logos/X2rBH_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Narciso rodríguez</span>
                            </div>
                                                                                <div id="letra_N" class="nmarca letra_N div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Natural honey" data-nombre_marca_id="1755" data-logo="logos/logo_7639_20220622092704.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Natural honey</span>
                            </div>
                                                                                <div id="letra_N" class="nmarca letra_N div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Nautica" data-nombre_marca_id="1025" data-logo="logos/logo_1025_20150611162521.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Nautica</span>
                            </div>
                                                                                <div id="letra_N" class="nmarca letra_N div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Nike" data-nombre_marca_id="259" data-logo="logos/logo_259_20150526084524.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Nike</span>
                            </div>
                                                                                <div id="letra_N" class="nmarca letra_N div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Nikos" data-nombre_marca_id="91" data-logo="logos/logo_91_20150525095232.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Nikos</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_O">O</div>
                                                            <div id="letra_O" class="nmarca letra_O div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Oscar de la renta" data-nombre_marca_id="94" data-logo="logos/logo_94_20150525095141.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Oscar de la renta</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_P">P</div>
                                                            <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Pacha ibiza" data-nombre_marca_id="96" data-logo="logos/logo_96_20150525095109.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Pacha ibiza</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Paco rabanne" data-nombre_marca_id="97" data-logo="logos/4pqsH_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Paco rabanne</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Paloma picasso" data-nombre_marca_id="98" data-logo="logos/logo_98_20150525095021.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Paloma picasso</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Pepe jeans" data-nombre_marca_id="1745" data-logo="logos/logo_7629_20220607125113.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Pepe jeans</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Perry ellis" data-nombre_marca_id="273" data-logo="logos/logo_273_20150525171748.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Perry ellis</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Pertegaz" data-nombre_marca_id="168" data-logo="logos/logo_168_20150525112413.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Pertegaz</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Philipp plein" data-nombre_marca_id="2129" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Philipp plein</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Playboy" data-nombre_marca_id="104" data-logo="logos/logo_104_20150525094831.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Playboy</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Police" data-nombre_marca_id="105" data-logo="logos/logo_105_20150525094757.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Police</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Prada" data-nombre_marca_id="106" data-logo="logos/bDd3s_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Prada</span>
                            </div>
                                                                                <div id="letra_P" class="nmarca letra_P div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Puig" data-nombre_marca_id="109" data-logo="logos/PXXmg_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Puig</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_Q">Q</div>
                                                            <div id="letra_Q" class="nmarca letra_Q div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Quorum" data-nombre_marca_id="110" data-logo="logos/logo_110_20150525101757.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Quorum</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_R">R</div>
                                                            <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Rabanne" data-nombre_marca_id="97" data-logo="logos/4pqsH_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Rabanne</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Ralph lauren" data-nombre_marca_id="111" data-logo="logos/9y9IS_2024-05-29.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Ralph lauren</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Rasasi" data-nombre_marca_id="2627" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Rasasi</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Real madrid" data-nombre_marca_id="1826" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Real madrid</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Real madrid c.f." data-nombre_marca_id="2324" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Real madrid c.f.</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Reebok" data-nombre_marca_id="1719" data-logo="logos/logo_7603_20220510150953.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Reebok</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Roberto cavalli" data-nombre_marca_id="115" data-logo="logos/logo_115_20150525101916.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Roberto cavalli</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Rochas" data-nombre_marca_id="117" data-logo="logos/pyKtO_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Rochas</span>
                            </div>
                                                                                <div id="letra_R" class="nmarca letra_R div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Rodríguez" data-nombre_marca_id="90" data-logo="logos/X2rBH_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Rodríguez</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_S">S</div>
                                                            <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Salvatore ferragamo" data-nombre_marca_id="119" data-logo="logos/logo_119_20150525102645.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Salvatore ferragamo</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Saphir" data-nombre_marca_id="4199" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Saphir</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Scalpers" data-nombre_marca_id="1597" data-logo="logos/9hKVJ_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Scalpers</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Schlesser" data-nombre_marca_id="7" data-logo="logos/oUmEB_2024-05-31.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Schlesser</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Serge lutens" data-nombre_marca_id="1218" data-logo="logos/logo_7069_20151022154121.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Serge lutens</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Sergio tacchini" data-nombre_marca_id="269" data-logo="logos/logo_269_20150525172105.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Sergio tacchini</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Sisley" data-nombre_marca_id="122" data-logo="logos/bZBum_2024-05-27.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Sisley</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Sportman" data-nombre_marca_id="3411" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Sportman</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Springfield" data-nombre_marca_id="1170" data-logo="logos/logo_1170_20150701135830.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Springfield</span>
                            </div>
                                                                                <div id="letra_S" class="nmarca letra_S div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Swiss arabian" data-nombre_marca_id="4172" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Swiss arabian</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_T">T</div>
                                                            <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Tabac original
" data-nombre_marca_id="127" data-logo="logos/logo_127_20150525102908.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Tabac original
</span>
                            </div>
                                                                                <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Ted lapidus" data-nombre_marca_id="128" data-logo="logos/logo_128_20150525102921.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Ted lapidus</span>
                            </div>
                                                                                <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Thierry mugler" data-nombre_marca_id="129" data-logo="logos/FHNuE_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Thierry mugler</span>
                            </div>
                                                                                <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Tom ford" data-nombre_marca_id="130" data-logo="logos/tEyXu_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Tom ford</span>
                            </div>
                                                                                <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Tommy hilfiger" data-nombre_marca_id="131" data-logo="logos/Lbkcq_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Tommy hilfiger</span>
                            </div>
                                                                                <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Tous" data-nombre_marca_id="132" data-logo="logos/mWpp8_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Tous</span>
                            </div>
                                                                                <div id="letra_T" class="nmarca letra_T div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Trussardi" data-nombre_marca_id="133" data-logo="logos/logo_133_20150525111308.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Trussardi</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_U">U</div>
                                                            <div id="letra_U" class="nmarca letra_U div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="United colors of benetton" data-nombre_marca_id="227" data-logo="logos/logo_227_20150525125942.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>United colors of benetton</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_V">V</div>
                                                            <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Valentino" data-nombre_marca_id="134" data-logo="logos/logo_134_20150525111330.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Valentino</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Van cleef &amp; arpels" data-nombre_marca_id="135" data-logo="logos/logo_135_20150525111349.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Van cleef &amp; arpels</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Varon dandy" data-nombre_marca_id="1797" data-logo="logos/logo_7681_20220727125545.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Varon dandy</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Versace" data-nombre_marca_id="138" data-logo="logos/obJ0N_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Versace</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Victor" data-nombre_marca_id="310" data-logo="logos/logo_310_20150611113546.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Victor</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Victorinox" data-nombre_marca_id="1037" data-logo="logos/logo_1037_20150609101506.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Victorinox</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Victorio &amp; lucchino" data-nombre_marca_id="140" data-logo="logos/logo_140_20150525111901.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Victorio &amp; lucchino</span>
                            </div>
                                                                                <div id="letra_V" class="nmarca letra_V div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Viktor &amp; rolf" data-nombre_marca_id="141" data-logo="logos/logo_119_20151020154421.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Viktor &amp; rolf</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_X">X</div>
                                                            <div id="letra_X" class="nmarca letra_X div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Xerjoff" data-nombre_marca_id="4163" data-logo="">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Xerjoff</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_Y">Y</div>
                                                            <div id="letra_Y" class="nmarca letra_Y div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Yacht man" data-nombre_marca_id="148" data-logo="logos/logo_148_20150525120747.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Yacht man</span>
                            </div>
                                                                                <div id="letra_Y" class="nmarca letra_Y div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Yves saint laurent" data-nombre_marca_id="143" data-logo="logos/60rYq_2024-05-28.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Yves saint laurent</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_Z">Z</div>
                                                            <div id="letra_Z" class="nmarca letra_Z div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="Zadig &amp; voltaire" data-nombre_marca_id="1285" data-logo="logos/lX6Oy_2024-05-30.jpg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>Zadig &amp; voltaire</span>
                            </div>
                                                                                    <div class="letra_cabecera letra_cabecera_0">0</div>
                                                            <div id="letra_0" class="nmarca letra_0 div_selector div_selector_marca  hijo_selector hijo_selector_scroll_texto" data-nombre_marca="4711" data-nombre_marca_id="1" data-logo="logos/logo_1_20150525094658.jpeg">
                                <i class="fa fa-circle-thin" aria-hidden="true"></i> <span>4711</span>
                            </div>
                                            </div>"""

brands = extract_fragrance_brands(html_content)
print(brands)
