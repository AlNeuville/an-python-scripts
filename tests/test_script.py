from app.model import ScriptFactory


def test_create_script():
	script = ScriptFactory.create_script('test', 'application args')
	assert script.name == 'test'
	assert script.application == 'application'
	assert script.arguments == ['args']
