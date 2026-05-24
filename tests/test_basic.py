import unittest

from android_automation import AndroidSearchAutomator, BUSCADORES, NAVEGADORES_ANDROID
from config_manager import ajustar_niveis, config_padrao
from search_generator import gerar_pesquisa


class ConfigManagerTests(unittest.TestCase):
    def test_config_padrao_tem_chaves_principais(self):
        config = config_padrao()

        self.assertIn("navegadores", config)
        self.assertIn("pc_modo_pesquisa", config)
        self.assertIn("android_buscador", config)
        self.assertIn("android_navegadores", config)

    def test_ajustar_niveis_completa_e_limita(self):
        self.assertEqual(ajustar_niveis(["2"], 3), ["2", "1", "1"])
        self.assertEqual(ajustar_niveis(["2", "1", "2"], 2), ["2", "1"])


class SearchGeneratorTests(unittest.TestCase):
    def test_gerar_pesquisa_retorna_texto(self):
        pesquisa = gerar_pesquisa()

        self.assertIsInstance(pesquisa, str)
        self.assertGreater(len(pesquisa.strip()), 5)


class AndroidAutomationTests(unittest.TestCase):
    def test_bing_existe_como_buscador_e_navegador(self):
        self.assertIn("Bing", BUSCADORES)
        self.assertIn("Bing", NAVEGADORES_ANDROID)
        self.assertEqual(NAVEGADORES_ANDROID["Bing"], "com.microsoft.bing")

    def test_formatar_texto_adb_normaliza_entrada(self):
        automator = AndroidSearchAutomator()

        self.assertEqual(
            automator.formatar_texto_adb("programacao avancada 2026!"),
            "programacao%savancada%s2026"
        )


if __name__ == "__main__":
    unittest.main()
