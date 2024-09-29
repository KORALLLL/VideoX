import { useTheme } from '@chakra-ui/react'
import { useState } from 'react'
import { CloudUpload, Cross } from 'shared/iconpack'
import { Flex, Text, Input, Button } from 'shared/ui'
import { useVideoUpload } from '../lib'

function AddFile() {
  const theme = useTheme()
  const gray600 = theme.colors?.gray['600']
  const [file, setFile] = useState<File | null>(null)
  const [name, setName] = useState<string>()
  const { uploadVideo } = useVideoUpload()

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
    }
  }

  const handleSaveClick = () => {
    if (file && name) {
      uploadVideo(name, file)
      setFile(null)
    }
  }

  const handleCancelClick = () => {
    setFile(null)
  }

  return (
    <Flex
      w={'100%'}
      minH={'430px'}
      p={'40px'}
      flexDir={'column'}
      bg={'gray.200'}
      filter={`drop-shadow(0 0 4px #BFC1C5)`}
      borderRadius={'10px'}
      mb={'30px'}
    >
      <Input
        type="text"
        maxW={'340px'}
        mb={'24px'}
        fontSize={'14px'}
        color={'gray.600'}
        value={name}
        placeholder="Введите название проекта"
        variant="unstyled"
        borderBottom={'1px solid'}
        borderRadius={'0'}
        borderColor={'gray.600'}
        onChange={(e) => setName(e.target.value)}
      />
      {file && (
        <Flex gap={'3px'}>
          <Text
            fontSize={'14px'}
            mb={'33px'}
          >
            Файл: {file.name}
          </Text>
          <Cross color='#848486' cursor={'pointer'} onClick={handleCancelClick} />
        </Flex>
      )}
      <Flex
        w={'100%'}
        minW={'268px'}
        h={'100%'}
        mb={'34px'}
        // minH={'215px'}
        flexDir={'column'}
        gap={'20px'}
        bg={'gray.200'}
        alignItems={'center'}
        justifyContent={'center'}
        position={'relative'}
        borderRadius={'10px'}
        border={'1px dashed white'}
        filter={'drop-shadow(0px 0px 10px rgba(81, 172, 239, .1))'}
      >
        <Flex flexDir={'column'} alignItems={'center'}>
          <Text
            fontSize={'20px'}
            align={'center'}
          >
            Нажмите для загрузки
            <br />
            или перенесите файл в это окно
          </Text>
          <Text fontSize={'20px'} fontWeight={600}>
            MP4
          </Text>
        </Flex>
        <CloudUpload color={gray600}/>
        <Input
          type="file"
          accept=".mp4"
          onChange={handleFileChange}
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            top: 0,
            left: 0,
            opacity: 0,
            cursor: 'pointer',
          }}
        />
      </Flex>
      <Flex gap={'26px'} justifyContent={'flex-end'} alignItems={'center'}>
        <Text
          fontSize={'14px'}
          fontWeight={600}
          color={'gray.600'}
          cursor={'pointer'}
          _hover={{ color: 'gray.500' }}
          onClick={handleCancelClick}
        >
          Отмена
        </Text>
        <Button
          fontSize={'14px'}
          fontWeight={700}
          isDisabled={!file || !name}
          onClick={handleSaveClick}
        >
          Отправить видео
        </Button>
      </Flex>
    </Flex>
  )
}

export default AddFile
