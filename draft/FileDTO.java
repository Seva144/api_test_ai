package ru.cbr.msk.lunohod.aiTest.dto.ui.response.file;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;
import ru.cbr.msk.lunohod.aiTest.dto.error.ErrorType;

import java.time.LocalDateTime;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@Builder
public class FileDTO {

    private String id;
    private String conversationId;
    private String filename;
    private String originalFilename;
    private Long fileSize;
    private String mimeType;
    private String processingStatus;
    private String content;
    private String summary;
    private LocalDateTime createdAt;
    private Map<String, Object> metadata;

    private ErrorType error;
    private String errorMessage;
}
